#include <gtest/gtest.h>

#include "hlp_test.hpp"

auto constexpr NAME = "ignoreParser";

INSTANTIATE_TEST_SUITE_P(IgnoreBuild,
                         HlpBuildTest,
                         ::testing::Values(BuildT(FAILURE, getIgnoreParser, {NAME, "", {}, {}}),
                                           BuildT(SUCCESS, getIgnoreParser, {NAME, "", {}, {"ignore"}}),
                                           BuildT(FAILURE, getIgnoreParser, {NAME, "", {}, {"ignore", "unexpected"}}),
                                           BuildT(FAILURE, getIgnoreParser, {NAME, "not allow", {}, {"ignore"}})));

INSTANTIATE_TEST_SUITE_P(
    IgnoreParse,
    HlpParseTest,
    ::testing::Values(ParseT(SUCCESS, "xcyber360", j("{}"), 5, getIgnoreParser, {NAME, "", {}, {"xcyber360"}}),
                      ParseT(SUCCESS, "xcyber360 123", j("{}"), 5, getIgnoreParser, {NAME, "", {}, {"xcyber360"}}),
                      ParseT(SUCCESS, "xcyber360xcyber360", j("{}"), 10, getIgnoreParser, {NAME, "", {}, {"xcyber360"}}),
                      ParseT(SUCCESS, "xcyber360xcyber360xcyber360xcyber360", j("{}"), 20, getIgnoreParser, {NAME, "", {}, {"xcyber360"}}),
                      ParseT(SUCCESS, "xcyber360wa", j("{}"), 5, getIgnoreParser, {NAME, "", {}, {"xcyber360"}}),
                      ParseT(FAILURE, "XCYBER360", j("{}"), 0, getIgnoreParser, {NAME, "", {}, {"xcyber360"}})));
