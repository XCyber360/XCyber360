
#ifndef _PARSE_EVENT_H
#define _PARSE_EVENT_H

#include <string>

#include <base/baseTypes.hpp>

namespace base::parseEvent
{
constexpr char EVENT_QUEUE_ID[] {"/xcyber360/queue"};
constexpr char EVENT_LOCATION_ID[] {"/xcyber360/location"};
constexpr char EVENT_MESSAGE_ID[] {"/event/original"};

/**
 * @brief Parse an Xcyber360 message and extract the queue, location and message
 *
 * @param event Xcyber360 message
 * @return Event Event object
 */
Event parseXcyber360Event(const std::string& event);

} // namespace base::parseEvent

#endif // _EVENT_UTILS_H
