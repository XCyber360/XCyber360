# frozen_string_literal: true

describe 'opendistro::repository' do
  case os.family
  when 'debian'
    describe apt('https://packages.xcyber360.com/4.x/apt/') do
      it { should exist }
      it { should be_enabled }
    end
  when 'redhat', 'suse'
    describe yum.repo('xcyber360') do
      it { should exist }
      it { should be_enabled }
    end
  end
end
