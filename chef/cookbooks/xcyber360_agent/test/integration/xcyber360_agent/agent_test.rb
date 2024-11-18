describe package('xcyber360-agent') do
    it { should be_installed }
end

describe service('xcyber360-agent') do
    it { should be_installed }
    it { should be_enabled }
    it { should be_running }
end