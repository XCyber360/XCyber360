#ifndef _COMPONENT_FAKE_STORE_HPP
#define _COMPONENT_FAKE_STORE_HPP

constexpr auto ROUTER_JSON {R"([])"};

constexpr auto TESTER_JSON {R"([])"};

constexpr auto POLICY_JSON {
    R"({"name":"policy/xcyber360/0","hash":"12403460954181119054","assets":["integration/xcyber360-core-fake/0"]})"};

constexpr auto FILTER_JSON {R"({
    "name": "filter/allow-all/0"
})"};

constexpr auto EPS_JSON {
    R"({
    "eps": 1,
    "refreshInterval": 1,
    "active": false
})"};

constexpr auto INTEGRATION_JSON {R"({
"name": "integration/xcyber360-core-fake/0",
"decoders": ["decoder/fake/0"]}
)"};

auto constexpr DECODER_JSON = R"e({
    "name": "decoder/fake/0",
    "normalize": [
        {
        "map": [
            {
            "xcyber360.message": "I am an fake decoder"
            }
        ]
        }
    ]
    })e";

auto constexpr XCYBER360_LOGPAR_TYPES_JSON = R"({
    "fields": {
        "xcyber360.message": "text"
    }
}
)";

#endif // _COMPONENT_FAKE_STORE_HPP
