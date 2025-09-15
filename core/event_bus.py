# core/event_bus.py
class EventBus:
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, event_name, callback):
        self.subscribers.setdefault(event_name, []).append(callback)

    def publish(self, event_name, *args, **kwargs):
        for cb in self.subscribers.get(event_name, []):
            try:
                cb(*args, **kwargs)
            except Exception as e:
                print(f"[EventBus] Error in {event_name} subscriber: {e}")

# A global singleton
event_bus = EventBus()
