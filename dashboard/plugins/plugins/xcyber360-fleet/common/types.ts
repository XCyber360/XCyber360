export type Agent = {
  agent: {
    id: string;
    name: string;
    version: string;
  };
  host: {
    os: {
      full: string;
      name: string;
      platform: string;
    };
    ip: string;
  };
  xcyber360: {};
  groups: string[];
};
