describe package('xcyber360-manager') do
    it { should be_installed }
end

describe service('xcyber360-manager') do
    it { should be_installed }
    it { should be_enabled }
    it { should be_running }
end

describe port(55000) do
    it { should be_listening }
    its('processes') {should include 'python3'}
end

describe port(1515) do
    it { should be_listening }
    its('processes') {should include 'xcyber360-authd'}
end

describe port(1514) do
    it { should be_listening }
    its('processes') {should include 'xcyber360-remoted'}
end
