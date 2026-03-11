"""Message bus module for decoupled channel-agent communication."""

from gssbot.bus.events import InboundMessage, OutboundMessage
from gssbot.bus.queue import MessageBus

__all__ = ["MessageBus", "InboundMessage", "OutboundMessage"]
