"""Message bus module for decoupled channel-agent communication."""

from biralo.bus.events import InboundMessage, OutboundMessage
from biralo.bus.queue import MessageBus

__all__ = ["MessageBus", "InboundMessage", "OutboundMessage"]
