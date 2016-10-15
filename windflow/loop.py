import asyncio


def get_event_loop(debug=False):
    if not debug:
        import uvloop
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        asyncio.set_event_loop(uvloop.new_event_loop())
    return asyncio.get_event_loop()
