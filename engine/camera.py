import glm
import pygame as pg


class Camera:
    def __init__(self, app,
                 FOV=50, NEAR=0.1, FAR=100, SPEED=0.01, ANGULAR_SPEED=0.05,
                 position=(0, 40, 0), yaw=-90, pitch=-90):
        self.app = app
        self.aspect_ratio = app.WIN_SIZE[0] / app.WIN_SIZE[1]

        # Store important Camera data
        self.fov = FOV # Degrees
        self.near_dist = NEAR
        self.far_dist = FAR
        self.speed = SPEED
        self.angular_speed = ANGULAR_SPEED

        # Set position vector, direction vectors, and camera angles
        self.position = glm.vec3(position)
        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)
        self.forward = glm.vec3(0, 0, -1)
        self.yaw = yaw
        self.pitch = pitch

        # Initialize projection and view matrices
        self.set_matrices()

    def set_matrices(self):
        # Get projection and view matrices
        self.view_matrix = self.get_view_matrix()
        self.projection_matrix = self.get_projection_matrix()

    def get_view_matrix(self):
        # glm.vec3(0) -> world center
        return glm.lookAt(self.position, self.position + self.forward, self.up)

    def get_projection_matrix(self):
        return glm.perspective(glm.radians(self.fov), self.aspect_ratio, self.near_dist, self.far_dist)

    def update(self):
        # self.move()
        # self.rotate()
        self.update_camera_vectors()
        self.view_matrix = self.get_view_matrix()

    def update_camera_vectors(self):
        yaw = glm.radians(self.yaw)
        pitch = glm.radians(self.pitch)

        self.forward.x = glm.cos(pitch) * glm.cos(yaw)
        self.forward.y = glm.sin(pitch)
        self.forward.z = glm.cos(pitch) * glm.sin(yaw)

        self.forward = glm.normalize(self.forward)
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0, 1, 0)))
        self.up = glm.normalize(glm.cross(self.right, self.forward))

    def move(self, keys):
        velocity = self.speed * self.app.delta_time_ms
        scroll_velocity = velocity * 10
        # keys = pg.key.get_pressed()
        '''if keys[pg.]:
            self.position += self.forward * velocity
        if keys[pg.K_s]:
            self.position -= self.forward * velocity'''
        # print(pg.event.get())
        # print('running camera move function')
        if self.app.scrolling != 0:
            self.position += self.forward * scroll_velocity * self.app.scrolling
            self.app.scrolling = 0
        if keys[pg.K_a]:
            self.position -= self.right * velocity
        if keys[pg.K_d]:
            self.position += self.right * velocity
        if keys[pg.K_w]:
            self.position += self.up * velocity
        if keys[pg.K_s]:
            self.position -= self.up * velocity

    def rotate(self):
        angular_velocity = self.angular_speed * self.app.delta_time_ms
        keys = pg.key.get_pressed()

        '''# Determine and limit pitch angle
        if keys[pg.K_UP]:
            self.pitch += angular_velocity
        elif keys[pg.K_DOWN]:
            self.pitch -= angular_velocity
        self.pitch = max(-90, min(90, self.pitch))

        # Deal with yaw
        if keys[pg.K_LEFT]:
            self.yaw -= angular_velocity
        elif keys[pg.K_RIGHT]:
            self.yaw += angular_velocity'''


