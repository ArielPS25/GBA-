
# ================================================================
# IMÁGENES
# ================================================================

image gba_background = "gba/background.png"
image gba_level = "gba/level.png"

image gba_idle = "gba/sprites/idle.png"
image gba_walk1 = "gba/sprites/walk1.png"
image gba_walk2 = "gba/sprites/walk2.png"
image gba_jump = "gba/sprites/jump.png"
image gba_fall = "gba/sprites/fall.png"
image gba_death = "gba/sprites/death.png"

image gba_gameover = "gba/gameover.png"
image gba_layoutgba = "gba/layoutgba.png"

# ================================================================
# PLATAFORMAS
# ================================================================

init python:

    gba_platforms = [

        (104, 52, 32, 28),

        (90, 80, 46, 80),

        (136, 88, 16, 72),

        (152, 104, 16, 56),

        (168, 120, 16, 40),

        (184, 136, 16, 24),

    ]


# ================================================================
# CLASE DEL MINIJUEGO
# ================================================================

init python:

    import pygame
    import time


    class GbaPlatformer(renpy.Displayable):


        # ========================================================
        # INICIALIZAR
        # ========================================================

        def __init__(self):

            super(GbaPlatformer, self).__init__()

            self.lives = 1

            self.game_over = False

            self.game_over_time = 0

            # Indica que ya terminó el Game Over

            self.game_over_finished = False

            self.reset_player()


        # ========================================================
        # REINICIAR JUGADOR
        # ========================================================

        def reset_player(self):

            self.player_x = 112
            self.player_y = 28

            self.velocity_y = 0

            self.on_ground = True

            self.walk_timer = 0
            self.walk_frame = 0

            self.facing = 1

            self.moving = False

            self.dead = False


            # ====================================================
            # DATOS DE MUERTE
            # ====================================================

            self.death_time = 0

            self.death_x = 112
            self.death_y = 28

            self.death_velocity_y = -5

            self.death_gravity = 0.35

            # True = timeout
            # False = caída al abismo

            self.timeout_death = False


            # ====================================================
            # ANIMACIÓN DE MUERTE
            # ====================================================

            self.death_frame = 0

            self.death_frame_timer = 0


            # ====================================================
            # TIMER DE PRUEBA
            # ====================================================

            self.game_time = 10.0

            self.last_time = time.time()


        # ========================================================
        # VISIT
        # ========================================================

        def visit(self):

            return [

                renpy.displayable("gba_background"),

                renpy.displayable("gba_level"),

                renpy.displayable("gba_idle"),

                renpy.displayable("gba_walk1"),

                renpy.displayable("gba_walk2"),

                renpy.displayable("gba_jump"),

                renpy.displayable("gba_fall"),

                renpy.displayable("gba_death"),

                renpy.displayable("gba_gameover"),

            ]


        # ========================================================
        # FUNCIÓN MORIR
        # ========================================================

        def player_die(self, timeout):

            self.dead = True

            self.timeout_death = timeout

            self.death_time = time.time()

            self.death_x = self.player_x

            self.death_y = self.player_y

            self.death_velocity_y = -5

            self.death_frame = 0

            self.death_frame_timer = 0


            # Restar una vida

            self.lives -= 1


            # Detener música del nivel

            renpy.music.stop()


            # Sonido de muerte

            renpy.sound.play(
                "gba/music/muerte.wav"
            )


        # ========================================================
        # RENDER
        # ========================================================

        def render(self, width, height, st, at):


            # ====================================================
            # GAME OVER
            # ====================================================

            if self.game_over:


                # ------------------------------------------------
                # COMPROBAR TIEMPO
                # ------------------------------------------------

                if (

                    time.time() - self.game_over_time >= 5.0

                    and not self.game_over_finished

                ):

                    self.game_over_finished = True
                    renpy.restart_interaction()


                # ------------------------------------------------
                # PANTALLA GAME OVER
                # ------------------------------------------------

                d = renpy.Render(
                    960,
                    640
                )


                gameover = Transform(

                    child="gba_gameover",

                    xsize=960,

                    ysize=640

                )


                gameover_render = renpy.render(

                    gameover,

                    960,

                    640,

                    st,

                    at

                )


                d.blit(

                    gameover_render,

                    (0, 0)

                )


                # ------------------------------------------------
                # ACTUALIZAR
                # ------------------------------------------------

                renpy.redraw(

                    self,

                    0.1

                )


                return d


            # ====================================================
            # TIMER
            # ====================================================

            if not self.dead:

                current_time = time.time()

                elapsed = current_time - self.last_time

                self.last_time = current_time

                self.game_time -= elapsed


                # ================================================
                # TIMEOUT
                # ================================================

                if self.game_time <= 0:

                    self.game_time = 0

                    self.player_die(
                        True
                    )


            # ====================================================
            # MUERTE
            # ====================================================

            if self.dead:


                # =================================================
                # ANIMACIÓN DE MUERTE
                # =================================================

                self.death_velocity_y += self.death_gravity

                self.death_y += self.death_velocity_y


                # =================================================
                # ANIMACIÓN DE BRAZOS
                # =================================================

                self.death_frame_timer += 1


                if self.death_frame_timer >= 8:

                    self.death_frame_timer = 0

                    self.death_frame += 1


                    if self.death_frame >= 2:

                        self.death_frame = 0


                # =================================================
                # DESPUÉS DE 5 SEGUNDOS
                # =================================================

                if time.time() - self.death_time >= 5.0:


                    renpy.sound.stop()


                    # =============================================
                    # TODAVÍA QUEDAN VIDAS
                    # =============================================

                    if self.lives > 0:


                        self.reset_player()


                        # Reiniciar música

                        renpy.music.play(

                            "gba/music/nivel.mp3",

                            loop=True

                        )


                    # =============================================
                    # NO QUEDAN VIDAS
                    # =============================================

                    else:


                        self.game_over = True

                        self.game_over_time = time.time()

                        self.game_over_finished = False


                        # Música Game Over

                        renpy.music.play(

                            "gba/music/gameover.mp3",

                            loop=False

                        )


            else:


                # =================================================
                # TECLADO
                # =================================================

                keys = pygame.key.get_pressed()

                self.moving = False


                # =================================================
                # DERECHA
                # =================================================

                if keys[pygame.K_RIGHT]:

                    self.player_x += 2

                    self.facing = 1

                    self.moving = True


                # =================================================
                # IZQUIERDA
                # =================================================

                if keys[pygame.K_LEFT]:

                    self.player_x -= 2

                    self.facing = -1

                    self.moving = True


                # =================================================
                # SALTO
                # =================================================

                if (

                    keys[pygame.K_SPACE]

                    or keys[pygame.K_UP]

                ) and self.on_ground:


                    self.velocity_y = -8

                    self.on_ground = False


                    renpy.sound.play(

                        "gba/music/jump.wav"

                    )


                # =================================================
                # GRAVEDAD
                # =================================================

                old_y = self.player_y

                self.velocity_y += 0.5

                self.player_y += self.velocity_y

                self.on_ground = False


                # =================================================
                # COLISIONES
                # =================================================

                player_left = self.player_x

                player_right = self.player_x + 16

                old_bottom = old_y + 24

                new_bottom = self.player_y + 24


                for platform in gba_platforms:


                    px, py, pw, ph = platform

                    platform_left = px

                    platform_right = px + pw

                    platform_top = py


                    if self.velocity_y >= 0:


                        if (

                            old_bottom <= platform_top

                            and new_bottom >= platform_top

                            and player_right > platform_left

                            and player_left < platform_right

                        ):


                            self.player_y = platform_top - 24

                            self.velocity_y = 0

                            self.on_ground = True

                            break


                # =================================================
                # ANIMACIÓN CAMINAR
                # =================================================

                if self.moving and self.on_ground:


                    self.walk_timer += 1


                    if self.walk_timer >= 10:


                        self.walk_timer = 0

                        self.walk_frame += 1


                        if self.walk_frame > 1:

                            self.walk_frame = 0


                else:


                    self.walk_timer = 0

                    self.walk_frame = 0


                # =================================================
                # CAÍDA AL ABISMO
                # =================================================

                if self.player_y > 160:

                    self.player_die(
                        False
                    )


            # ====================================================
            # CREAR CANVAS GBA
            # ====================================================

            d = renpy.Render(
                960,
                640
            )


            # ====================================================
            # BACKGROUND
            # ====================================================

            bg = Transform(

                child="gba_background",

                xsize=960,

                ysize=640
                

            )


            bg_render = renpy.render(

                bg,

                960,

                640,

                st,

                at

            )


            d.blit(

                bg_render,

                (0, 0)

            )


            # ====================================================
            # LEVEL
            # ====================================================

            level = Transform(

                child="gba_level",

                xsize=960,

                ysize=640

            )


            level_render = renpy.render(

                level,

                960,

                640,

                st,

                at

            )


            d.blit(

                level_render,

                (0, 0)

            )



            # ====================================================
            # SELECCIONAR SPRITE
            # ====================================================

            if self.dead:


                if self.timeout_death:

                    sprite_name = "gba_death"

                else:

                    sprite_name = None


            else:


                if self.velocity_y < 0:

                    sprite_name = "gba_jump"


                elif not self.on_ground:

                    sprite_name = "gba_fall"


                elif self.moving:


                    if self.walk_frame == 0:

                        sprite_name = "gba_walk2"

                    else:

                        sprite_name = "gba_walk1"


                else:

                    sprite_name = "gba_idle"


            # ====================================================
            # DIBUJAR MARIO
            # ====================================================

            if sprite_name is not None:


                # ================================================
                # MUERTE
                # ================================================

                if self.dead and self.timeout_death:


                    if self.death_frame == 0:

                        death_zoom = 1

                    else:

                        death_zoom = -1


                    sprite = Transform(

                        child="gba_death",

                        xzoom=death_zoom,

                        xsize=64,

                        ysize=96

                    )


                # ================================================
                # NORMAL
                # ================================================

                else:


                    sprite = Transform(

                        child=sprite_name,

                        xzoom=self.facing,

                        xsize=64,

                        ysize=96

                    )


                sprite_render = renpy.render(

                    sprite,

                    64,

                    96,

                    st,

                    at

                )


                # ================================================
                # POSICIÓN
                # ================================================

                if not self.dead:

                    draw_x = self.player_x

                    draw_y = self.player_y

                else:

                    draw_x = self.death_x

                    draw_y = self.death_y


                d.blit(

                    sprite_render,

                    (

                        draw_x * 4,

                        draw_y * 4

                    )

                )


            # ====================================================
            # TIMER
            # ====================================================

            if not self.dead:

                timer_text = Text(

                    "{:03d}".format(int(self.game_time)),

                    font="gba/Super-Mario-World.ttf",

                    size=32,

                    color="#ffffff",

                    outlines=[

                        (2, "#000000", 0, 0)

                    ]

                )

                timer_render = renpy.render(

                    timer_text,

                    120,

                    50,

                    st,

                    at

                )

                d.blit(

                    timer_render,

                    (

                        151 * 4,

                        9 * 4

                    )

                )
            # ====================================================
            # VIDAS
            # ====================================================
            # ====================================================
            # VIDAS
            # ====================================================

            if not self.dead:

                lives_text = Text(

                    "{:02d}".format(self.lives),

                    font="gba/Super-Mario-World.ttf",

                    size=32,

                    color="#ffffff",

                    outlines=[

                        (2, "#000000", 0, 0)

                    ]

                )

                lives_render = renpy.render(

                    lives_text,

                    120,

                    50,

                    st,

                    at

                )

                d.blit(

                    lives_render,

                    (

                        17 * 4,

                        9 * 4

                    )

                )




            # ====================================================
            # ACTUALIZAR
            # ====================================================

            renpy.redraw(

                self,

                0

            )


            return d


# ================================================================
# INSTANCIA
# ================================================================

default gba_game_obj = None


# ================================================================
# SCREEN
# ================================================================

screen gba_game():

    modal True

    add Solid("#000000")

    # ============================================================
    # PANTALLA DEL JUEGO
    # ============================================================

    add gba_game_obj:
        xpos 480
        ypos 220

    # ============================================================
    # MARCO / CARCASA GBA
    # ============================================================

    add "gba/layoutgba.png":
        xpos 0
        ypos 0

    # ------------------------------------------------------------
    # RETORNO AUTOMÁTICO TRAS GAME OVER
    # ------------------------------------------------------------

    if gba_game_obj and gba_game_obj.game_over_finished:
        timer 0.01 action Return("game_over")

    if not gba_game_obj.game_over:

        text "← →  Mover     ESPACIO / ↑  Saltar":
            xalign 0.5
            yalign 0.97
            size 22
            color "#ffffff"

    key "K_ESCAPE" action Return()
# ================================================================
# LABEL
# ================================================================

label juego_gba:

    $ gba_game_obj = GbaPlatformer()

    play music "gba/music/nivel.mp3" loop

    call screen gba_game

    stop music

    return

