"""
Engine v3 - Core game engine implementation
"""
import math
import time
import random
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class EngineState(Enum):
    UNINITIALIZED = 0
    INITIALIZING = 1
    RUNNING = 2
    PAUSED = 3
    STOPPING = 4
    STOPPED = 5


class ComponentType(Enum):
    TRANSFORM = "transform"
    RENDERER = "renderer"
    PHYSICS = "physics"
    COLLIDER = "collider"
    SCRIPT = "script"
    AUDIO = "audio"


@dataclass
class Vector3:
    x: float
    y: float
    z: float

    def magnitude(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def normalize(self) -> 'Vector3':
        mag = self.magnitude()
        if mag == 0:
            return Vector3(0, 0, 0)
        return Vector3(self.x / mag, self.y / mag, self.z / mag)

    def dot(self, other: 'Vector3') -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: 'Vector3') -> 'Vector3':
        return Vector3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def __add__(self, other: 'Vector3') -> 'Vector3':
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: 'Vector3') -> 'Vector3':
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar: float) -> 'Vector3':
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)


@dataclass
class Quaternion:
    w: float
    x: float
    y: float
    z: float

    def conjugate(self) -> 'Quaternion':
        return Quaternion(self.w, -self.x, -self.y, -self.z)

    def magnitude(self) -> float:
        return math.sqrt(self.w ** 2 + self.x ** 2 + self.y ** 2 + self.z ** 2)

    def normalize(self) -> 'Quaternion':
        mag = self.magnitude()
        return Quaternion(self.w / mag, self.x / mag, self.y / mag, self.z / mag)

    def multiply(self, other: 'Quaternion') -> 'Quaternion':
        w = self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z
        x = self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y
        y = self.w * other.y - self.x * other.z + self.y * other.w + self.z * other.x
        z = self.w * other.z + self.x * other.y - self.y * other.x + self.z * other.w
        return Quaternion(w, x, y, z)


class Transform:
    def __init__(self):
        self.position = Vector3(0, 0, 0)
        self.rotation = Quaternion(1, 0, 0, 0)
        self.scale = Vector3(1, 1, 1)
        self.parent: Optional['Transform'] = None
        self.children: List['Transform'] = []

    def translate(self, offset: Vector3):
        self.position = self.position + offset

    def rotate(self, rotation: Quaternion):
        self.rotation = self.rotation.multiply(rotation)

    def get_world_position(self) -> Vector3:
        if self.parent is None:
            return self.position
        parent_pos = self.parent.get_world_position()
        return parent_pos + self.position

    def get_forward(self) -> Vector3:
        return Vector3(0, 0, 1)

    def get_right(self) -> Vector3:
        return Vector3(1, 0, 0)

    def get_up(self) -> Vector3:
        return Vector3(0, 1, 0)

    def look_at(self, target: Vector3):
        direction = (target - self.position).normalize()
        # Simplified look-at calculation
        pass


class Component:
    def __init__(self, entity_id: int):
        self.entity_id = entity_id
        self.enabled = True
        self.component_type = ComponentType.TRANSFORM

    def on_create(self):
        pass

    def on_update(self, delta_time: float):
        pass

    def on_destroy(self):
        pass

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False


class RenderComponent(Component):
    def __init__(self, entity_id: int):
        super().__init__(entity_id)
        self.component_type = ComponentType.RENDERER
        self.mesh_id = None
        self.material_id = None
        self.visible = True
        self.cast_shadows = True
        self.receive_shadows = True

    def set_mesh(self, mesh_id: int):
        self.mesh_id = mesh_id

    def set_material(self, material_id: int):
        self.material_id = material_id

    def render(self):
        if not self.visible or not self.enabled:
            return
        # Rendering logic here
        pass


class PhysicsComponent(Component):
    def __init__(self, entity_id: int):
        super().__init__(entity_id)
        self.component_type = ComponentType.PHYSICS
        self.velocity = Vector3(0, 0, 0)
        self.acceleration = Vector3(0, 0, 0)
        self.mass = 1.0
        self.drag = 0.1
        self.use_gravity = True

    def apply_force(self, force: Vector3):
        self.acceleration = self.acceleration + (force * (1.0 / self.mass))

    def apply_impulse(self, impulse: Vector3):
        self.velocity = self.velocity + (impulse * (1.0 / self.mass))

    def on_update(self, delta_time: float):
        if not self.enabled:
            return

        # Apply gravity
        if self.use_gravity:
            gravity = Vector3(0, -9.81, 0)
            self.apply_force(gravity * self.mass)

        # Update velocity
        self.velocity = self.velocity + (self.acceleration * delta_time)

        # Apply drag
        drag_force = self.velocity * (-self.drag)
        self.velocity = self.velocity + drag_force

        # Reset acceleration
        self.acceleration = Vector3(0, 0, 0)


class ColliderComponent(Component):
    def __init__(self, entity_id: int):
        super().__init__(entity_id)
        self.component_type = ComponentType.COLLIDER
        self.is_trigger = False
        self.bounds_min = Vector3(-1, -1, -1)
        self.bounds_max = Vector3(1, 1, 1)

    def check_collision(self, other: 'ColliderComponent') -> bool:
        # Simple AABB collision
        return (
            self.bounds_min.x <= other.bounds_max.x and
            self.bounds_max.x >= other.bounds_min.x and
            self.bounds_min.y <= other.bounds_max.y and
            self.bounds_max.y >= other.bounds_min.y and
            self.bounds_min.z <= other.bounds_max.z and
            self.bounds_max.z >= other.bounds_min.z
        )

    def set_box_bounds(self, size: Vector3):
        half_size = size * 0.5
        self.bounds_min = half_size * -1
        self.bounds_max = half_size


class Entity:
    _next_id = 0

    def __init__(self, name: str = "Entity"):
        self.id = Entity._next_id
        Entity._next_id += 1
        self.name = name
        self.active = True
        self.components: Dict[ComponentType, Component] = {}
        self.transform = Transform()

    def add_component(self, component: Component):
        self.components[component.component_type] = component
        component.on_create()

    def get_component(self, component_type: ComponentType) -> Optional[Component]:
        return self.components.get(component_type)

    def remove_component(self, component_type: ComponentType):
        if component_type in self.components:
            self.components[component_type].on_destroy()
            del self.components[component_type]

    def update(self, delta_time: float):
        if not self.active:
            return
        for component in self.components.values():
            if component.enabled:
                component.on_update(delta_time)

    def destroy(self):
        for component in self.components.values():
            component.on_destroy()
        self.components.clear()


class Scene:
    def __init__(self, name: str):
        self.name = name
        self.entities: Dict[int, Entity] = {}
        self.root_entities: List[Entity] = []

    def create_entity(self, name: str = "Entity") -> Entity:
        entity = Entity(name)
        self.entities[entity.id] = entity
        self.root_entities.append(entity)
        return entity

    def destroy_entity(self, entity_id: int):
        if entity_id in self.entities:
            entity = self.entities[entity_id]
            entity.destroy()
            if entity in self.root_entities:
                self.root_entities.remove(entity)
            del self.entities[entity_id]

    def find_entity_by_name(self, name: str) -> Optional[Entity]:
        for entity in self.entities.values():
            if entity.name == name:
                return entity
        return None

    def get_all_entities(self) -> List[Entity]:
        return list(self.entities.values())

    def update(self, delta_time: float):
        for entity in self.entities.values():
            entity.update(delta_time)


class ResourceManager:
    def __init__(self):
        self.meshes: Dict[int, Dict] = {}
        self.materials: Dict[int, Dict] = {}
        self.textures: Dict[int, Dict] = {}
        self.sounds: Dict[int, Dict] = {}
        self._next_resource_id = 0

    def load_mesh(self, path: str) -> int:
        resource_id = self._next_resource_id
        self._next_resource_id += 1
        self.meshes[resource_id] = {
            'path': path,
            'vertices': [],
            'indices': [],
            'normals': [],
            'uvs': []
        }
        return resource_id

    def load_material(self, path: str) -> int:
        resource_id = self._next_resource_id
        self._next_resource_id += 1
        self.materials[resource_id] = {
            'path': path,
            'shader': None,
            'properties': {}
        }
        return resource_id

    def load_texture(self, path: str) -> int:
        resource_id = self._next_resource_id
        self._next_resource_id += 1
        self.textures[resource_id] = {
            'path': path,
            'width': 0,
            'height': 0,
            'data': None
        }
        return resource_id

    def unload_resource(self, resource_id: int):
        if resource_id in self.meshes:
            del self.meshes[resource_id]
        elif resource_id in self.materials:
            del self.materials[resource_id]
        elif resource_id in self.textures:
            del self.textures[resource_id]
        elif resource_id in self.sounds:
            del self.sounds[resource_id]

    def get_mesh(self, resource_id: int) -> Optional[Dict]:
        return self.meshes.get(resource_id)

    def get_material(self, resource_id: int) -> Optional[Dict]:
        return self.materials.get(resource_id)


class Renderer:
    def __init__(self):
        self.viewport_width = 1920
        self.viewport_height = 1080
        self.clear_color = (0.2, 0.3, 0.4, 1.0)
        self.render_queue: List[RenderComponent] = []

    def initialize(self):
        # Initialize rendering context
        pass

    def set_viewport(self, width: int, height: int):
        self.viewport_width = width
        self.viewport_height = height

    def clear(self):
        # Clear the screen
        self.render_queue.clear()

    def add_to_queue(self, render_component: RenderComponent):
        self.render_queue.append(render_component)

    def render_frame(self):
        # Sort render queue by material/distance
        for component in self.render_queue:
            component.render()
        self.render_queue.clear()

    def shutdown(self):
        # Cleanup rendering resources
        pass


class PhysicsEngine:
    def __init__(self):
        self.gravity = Vector3(0, -9.81, 0)
        self.physics_components: List[PhysicsComponent] = []
        self.collider_components: List[ColliderComponent] = []
        self.simulation_speed = 1.0

    def register_physics_component(self, component: PhysicsComponent):
        self.physics_components.append(component)

    def unregister_physics_component(self, component: PhysicsComponent):
        if component in self.physics_components:
            self.physics_components.remove(component)

    def register_collider(self, collider: ColliderComponent):
        self.collider_components.append(collider)

    def unregister_collider(self, collider: ColliderComponent):
        if collider in self.collider_components:
            self.collider_components.remove(collider)

    def simulate(self, delta_time: float):
        adjusted_dt = delta_time * self.simulation_speed

        # Update physics
        for component in self.physics_components:
            component.on_update(adjusted_dt)

        # Check collisions
        self.check_collisions()

    def check_collisions(self):
        for i in range(len(self.collider_components)):
            for j in range(i + 1, len(self.collider_components)):
                collider_a = self.collider_components[i]
                collider_b = self.collider_components[j]

                if collider_a.check_collision(collider_b):
                    self.on_collision(collider_a, collider_b)

    def on_collision(self, a: ColliderComponent, b: ColliderComponent):
        # Handle collision response
        pass

    def raycast(self, origin: Vector3, direction: Vector3, max_distance: float) -> Optional[Tuple[Entity, float]]:
        # Simple raycast implementation
        return None


class InputManager:
    def __init__(self):
        self.keys_down: Dict[str, bool] = {}
        self.keys_pressed: Dict[str, bool] = {}
        self.keys_released: Dict[str, bool] = {}
        self.mouse_position = Vector3(0, 0, 0)
        self.mouse_delta = Vector3(0, 0, 0)
        self.mouse_buttons: Dict[int, bool] = {}

    def update(self):
        # Clear frame-specific states
        self.keys_pressed.clear()
        self.keys_released.clear()

    def is_key_down(self, key: str) -> bool:
        return self.keys_down.get(key, False)

    def is_key_pressed(self, key: str) -> bool:
        return self.keys_pressed.get(key, False)

    def is_key_released(self, key: str) -> bool:
        return self.keys_released.get(key, False)

    def is_mouse_button_down(self, button: int) -> bool:
        return self.mouse_buttons.get(button, False)

    def get_mouse_position(self) -> Vector3:
        return self.mouse_position

    def get_mouse_delta(self) -> Vector3:
        return self.mouse_delta


class AudioEngine:
    def __init__(self):
        self.master_volume = 1.0
        self.music_volume = 1.0
        self.sfx_volume = 1.0
        self.active_sounds: Dict[int, Dict] = {}
        self._next_sound_id = 0

    def play_sound(self, sound_id: int, volume: float = 1.0, loop: bool = False) -> int:
        instance_id = self._next_sound_id
        self._next_sound_id += 1
        self.active_sounds[instance_id] = {
            'sound_id': sound_id,
            'volume': volume,
            'loop': loop,
            'position': 0.0
        }
        return instance_id

    def stop_sound(self, instance_id: int):
        if instance_id in self.active_sounds:
            del self.active_sounds[instance_id]

    def set_master_volume(self, volume: float):
        self.master_volume = max(0.0, min(1.0, volume))

    def update(self, delta_time: float):
        # Update sound playback
        for instance_id, sound_data in list(self.active_sounds.items()):
            sound_data['position'] += delta_time


class Engine:
    def __init__(self):
        self.state = EngineState.UNINITIALIZED
        self.target_fps = 60
        self.delta_time = 0.0
        self.time_scale = 1.0
        self.frame_count = 0

        # Subsystems
        self.resource_manager = ResourceManager()
        self.renderer = Renderer()
        self.physics_engine = PhysicsEngine()
        self.input_manager = InputManager()
        self.audio_engine = AudioEngine()

        # Scene management
        self.active_scene: Optional[Scene] = None
        self.scenes: Dict[str, Scene] = {}

    def initialize(self):
        self.state = EngineState.INITIALIZING
        self.renderer.initialize()
        self.state = EngineState.RUNNING

    def create_scene(self, name: str) -> Scene:
        scene = Scene(name)
        self.scenes[name] = scene
        return scene

    def load_scene(self, name: str):
        if name in self.scenes:
            self.active_scene = self.scenes[name]

    def run(self):
        last_time = time.time()

        while self.state == EngineState.RUNNING:
            current_time = time.time()
            self.delta_time = (current_time - last_time) * self.time_scale
            last_time = current_time

            self.update()
            self.render()

            self.frame_count += 1

            # Frame rate limiting
            target_frame_time = 1.0 / self.target_fps
            elapsed = time.time() - current_time
            if elapsed < target_frame_time:
                time.sleep(target_frame_time - elapsed)

    def update(self):
        if self.state != EngineState.RUNNING:
            return

        # Update input
        self.input_manager.update()

        # Update active scene
        if self.active_scene:
            self.active_scene.update(self.delta_time)

        # Update physics
        self.physics_engine.simulate(self.delta_time)

        # Update audio
        self.audio_engine.update(self.delta_time)

    def render(self):
        if self.state != EngineState.RUNNING:
            return

        self.renderer.clear()

        # Collect render components from active scene
        if self.active_scene:
            for entity in self.active_scene.get_all_entities():
                render_comp = entity.get_component(ComponentType.RENDERER)
                if render_comp and isinstance(render_comp, RenderComponent):
                    self.renderer.add_to_queue(render_comp)

        self.renderer.render_frame()

    def pause(self):
        if self.state == EngineState.RUNNING:
            self.state = EngineState.PAUSED

    def resume(self):
        if self.state == EngineState.PAUSED:
            self.state = EngineState.RUNNING

    def shutdown(self):
        self.state = EngineState.STOPPING
        self.renderer.shutdown()
        self.state = EngineState.STOPPED

    def get_fps(self) -> float:
        if self.delta_time > 0:
            return 1.0 / self.delta_time
        return 0.0
