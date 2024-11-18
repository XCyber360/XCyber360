import subprocess
import sys
from pathlib import Path
from google.protobuf.json_format import ParseDict
import json
from engine_handler.handler import EngineHandler
from api_communication.proto import catalog_pb2 as api_catalog
from api_communication.proto import engine_pb2 as api_engine
from api_communication.proto import policy_pb2 as api_policy
from api_communication.proto import router_pb2 as api_router


def load_filters(ruleset_path: Path, engine_handler: EngineHandler) -> None:
    for filter_file in (ruleset_path / 'filters').rglob('*.yml'):
        request = api_catalog.ResourcePost_Request()
        request.type = api_catalog.ResourceType.filter
        request.namespaceid = "system"
        request.content = filter_file.read_text()
        request.format = api_catalog.ResourceFormat.yml
        print(f"Loading filter...\n{request}")
        error, response = engine_handler.api_client.send_recv(request)
        if error:
            raise Exception(error)

        parsed_response = ParseDict(
            response, api_engine.GenericStatus_Response())
        if parsed_response.status == api_engine.ERROR:
            raise Exception(parsed_response.error)
        print(f"Filter loaded.")


def load_integrations(ruleset_path: Path, engine_handler: EngineHandler) -> None:
    for integration_dir in (ruleset_path / 'integrations').iterdir():
        ns = "system" if integration_dir.name == 'xcyber360-core' else "xcyber360"
        command_str = f'engine-integration add --api-sock {engine_handler.api_socket_path} --namespace {ns} {integration_dir.resolve().as_posix()}'
        print(f"Loading integration...\n{command_str}")
        subprocess.run(command_str, check=True, shell=True)
        print(f"Integration loaded.")


def load_policy(ruleset_path: Path, engine_handler: EngineHandler, stop_on_warn: bool) -> None:
    # Create policy
    request = api_policy.StorePost_Request()
    request.policy = "policy/xcyber360/0"
    print(f"Creating policy...\n{request}")
    error, response = engine_handler.api_client.send_recv(request)
    if error:
        raise Exception(error)
    parsed_response = ParseDict(response, api_engine.GenericStatus_Response())
    if parsed_response.status == api_engine.ERROR:
        raise Exception(parsed_response.error)
    print("Policy created.")

    # Set default parents for xcyber360 and user namespaces
    request = api_policy.DefaultParentPost_Request()
    request.parent = "decoder/integrations/0"
    request.namespace = "xcyber360"
    request.policy = "policy/xcyber360/0"
    print(f"Setting default parent...\n{request}")
    error, response = engine_handler.api_client.send_recv(request)
    if error:
        raise Exception(error)
    parsed_response = ParseDict(
        response, api_policy.DefaultParentPost_Response())
    if parsed_response.status == api_engine.ERROR:
        raise Exception(parsed_response.error)
    if len(parsed_response.warning) > 0 and stop_on_warn:
        raise Exception(parsed_response.warning)
    print("Default parent set.")

    request = api_policy.DefaultParentPost_Request()
    request.parent = "decoder/integrations/0"
    request.namespace = "user"
    request.policy = "policy/xcyber360/0"
    print(f"Setting default parent...\n{request}")
    error, response = engine_handler.api_client.send_recv(request)
    if error:
        raise Exception(error)
    parsed_response = ParseDict(
        response, api_policy.DefaultParentPost_Response())
    if parsed_response.status == api_engine.ERROR:
        raise Exception(parsed_response.error)
    if len(parsed_response.warning) > 0 and stop_on_warn:
        raise Exception(parsed_response.warning)
    print("Default parent set.")

    # Add xcyber360-core
    request = api_policy.AssetPost_Request()
    request.asset = "integration/xcyber360-core/0"
    request.policy = "policy/xcyber360/0"
    request.namespace = "system"
    print(f"Adding xcyber360-core...\n{request}")
    error, response = engine_handler.api_client.send_recv(request)
    if error:
        raise Exception(error)
    parsed_response = ParseDict(response, api_policy.AssetPost_Response())
    if parsed_response.status == api_engine.ERROR:
        raise Exception(parsed_response.error)
    if len(parsed_response.warning) > 0 and stop_on_warn:
        raise Exception(parsed_response.warning)
    print("xcyber360-core added.")

    # Add rest of integrations
    for integration_dir in (ruleset_path / 'integrations').iterdir():
        if integration_dir.name == 'xcyber360-core':
            continue

        integration_name = f'integration/{integration_dir.name}/0'
        request = api_policy.AssetPost_Request()
        request.asset = integration_name
        request.policy = "policy/xcyber360/0"
        request.namespace = "xcyber360"
        print(f"Adding {integration_name}...\n{request}")
        error, response = engine_handler.api_client.send_recv(request)
        if error:
            raise Exception(error)
        parsed_response = ParseDict(
            response, api_policy.AssetPost_Response())
        if parsed_response.status == api_engine.ERROR:
            raise Exception(parsed_response.error)
        if len(parsed_response.warning) > 0 and stop_on_warn:
            raise Exception(parsed_response.warning)
        print(f"{integration_name} added.")

    # Load environment
    request = api_router.RoutePost_Request()
    request.route.name = "default"
    request.route.policy = "policy/xcyber360/0"
    request.route.filter = "filter/allow-all/0"
    request.route.priority = 254
    request.route.description = "Default route"
    print(f"Loading environment...\n{request}")
    error, response = engine_handler.api_client.send_recv(request)
    if error:
        raise Exception(error)
    parsed_response = ParseDict(response, api_engine.GenericStatus_Response())
    if parsed_response.status == api_engine.ERROR:
        raise Exception(parsed_response.error)
    print("Environment loaded.")


def run(args):
    env_path = Path(args['environment']).resolve()

    conf_path = (env_path / "engine/general.conf").resolve()
    if not conf_path.is_file():
        print(f"Configuration file not found: {conf_path}")
        sys.exit(1)

    bin_path = (env_path / "bin/xcyber360-engine").resolve()
    if not bin_path.is_file():
        print(f"Engine binary not found: {bin_path}")
        sys.exit(1)

    ruleset_path = (env_path / "ruleset").resolve()
    if not ruleset_path.is_dir():
        print(f"Engine ruleset not found: {ruleset_path}")
        sys.exit(1)

    stop_on_warn = args.get('stop_on_warning', False)

    print("Starting the engine...")
    engine_handler = EngineHandler(
        bin_path.as_posix(), conf_path.as_posix())
    engine_handler.start()
    print("Engine started.")

    # Clear environmet
    command_str = f'engine-clear --api-sock {engine_handler.api_socket_path} -f'
    print(f"Clear environment...\n{command_str}")
    subprocess.run(command_str, check=True, shell=True)
    print(f"Environment cleared.")

    # Load filters
    load_filters(ruleset_path, engine_handler)

    # Load integrations
    load_integrations(ruleset_path, engine_handler)

    # Create policy
    load_policy(ruleset_path, engine_handler, stop_on_warn)

    print("Stopping the engine...")
    engine_handler.stop()
    print("Engine stopped.")