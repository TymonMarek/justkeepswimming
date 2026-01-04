import enum

from pygame import Surface

from justkeepswimming.utilities.image import Image, ImageRegion


class Keyframe:
    def __init__(self, timestamp: float, region: ImageRegion) -> None:
        self.timestamp: float = timestamp
        self.region: ImageRegion = region


class AnimationPriority(enum.Enum):
    RESERVED = 4
    HIGH = 3
    MEDIUM = 2
    LOW = 1
    NONE = 0


class KeyframeSequence:
    def __init__(self, keyframes: list[Keyframe]) -> None:
        self.keyframes: list[Keyframe] = sorted(
            keyframes, key=lambda keyframe: keyframe.timestamp
        )
        self.duration: float = max(keyframe.timestamp for keyframe in self.keyframes)

    def reverse(self) -> "KeyframeSequence":
        reversed_keyframes = [
            Keyframe(self.duration - keyframe.timestamp, keyframe.region)
            for keyframe in reversed(self.keyframes)
        ]
        return KeyframeSequence(reversed_keyframes)


class Animation:
    def __init__(
        self, texture: Image, sequence: KeyframeSequence, priority: AnimationPriority
    ) -> None:
        self.texture: Image = texture
        self.sequence: KeyframeSequence = sequence
        self.priority: AnimationPriority = priority
        self.looped: bool = True
        self.speed: float = 1.0


class AnimationTrack:
    def __init__(self, animation: Animation) -> None:
        self.animation: Animation = animation
        self.priority: AnimationPriority = animation.priority
        self.looped: bool = animation.looped
        self.speed: float = animation.speed
        self.frames: list[Surface] = []
        self.time: float = 0.0

    async def load(self) -> None:
        if not self.animation.texture.loaded:
            await self.animation.texture.load()

        for keyframe in self.animation.sequence.keyframes:
            self.frames.append(keyframe.region.slice(self.animation.texture))


class Animator:
    def __init__(self) -> None:
        self.tracks: list[AnimationTrack] = []

    async def load(self, animation: Animation) -> AnimationTrack:
        track = AnimationTrack(animation)
        await track.load()
        self.tracks.append(track)
        return track
