# Constants
REQUESTS_LIMIT = 60
TIMEFRAME_REQUESTS_MS = 60000

# Error codes and descriptions
errors = {
    400 : "Bad Request -- Your request is invalid.",
    404 : "Not Found -- The specified resource could not be found.",
    406 : "Not Acceptable -- You requested a format that isn't json.",
    429 : "Too Many Requests -- Stop bombarding us.",
    500 : "Internal Server Error -- We had a problem with our server. Try again later.",
    503 : "Service Unavailable -- We're temporarily offline for maintenance. Please try again later."
}