
import pygame
import struct
import math


class SoundGenerator:

    def __init__(self):
        self.sounds = {}
        self.sound_enabled = True

        try:
            self.generate_all_sounds()
        except Exception as e:
            print(f"⚠️ Не удалось создать звуки: {e}")
            import traceback
            traceback.print_exc()
            self.sound_enabled = False

    def create_beep(self, frequency, duration, volume=1.0):
        try:
            mixer_info = pygame.mixer.get_init()
            if mixer_info is None:
                return None

            sample_rate, format_bits, num_channels = mixer_info

            num_samples = int(sample_rate * duration)

            buf = []

            for i in range(num_samples):
                t = float(i) / sample_rate

                decay = math.exp(-5 * t / duration)

                fade_in_duration = 0.01
                if t < fade_in_duration:
                    fade_in = t / fade_in_duration
                else:
                    fade_in = 1.0

                value = math.sin(2.0 * math.pi * frequency * t) * decay * fade_in * volume

                sample_value = int(value * 16384)

                sample_bytes = struct.pack('<h', sample_value)

                if num_channels == 2:
                    buf.append(sample_bytes)
                    buf.append(sample_bytes)
                else:
                    buf.append(sample_bytes)

            sound_buffer = b''.join(buf)

            sound = pygame.mixer.Sound(buffer=sound_buffer)
            sound.set_volume(volume)

            return sound

        except Exception as e:
            print(f"      ❌ Ошибка создания звука: {e}")
            import traceback
            traceback.print_exc()
            return None

    def generate_all_sounds(self):
        print("🎵 Генерация звуков...")

        try:
            self.sounds['flap'] = self.create_beep(330, 0.08, 0.4)
            print("  ✅ Звук взмаха (мягкий)")

            self.sounds['score'] = self.create_beep(523, 0.15, 0.5)
            print("  ✅ Звук очка (приятный)")

            self.sounds['death'] = self.create_beep(165, 0.4, 0.5)
            print("  ✅ Звук смерти (низкий)")

            self.sounds['levelup'] = self.create_beep(659, 0.25, 0.6)
            print("  ✅ Звук повышения уровня (радостный)")

            self.sounds['menu_select'] = self.create_beep(440, 0.1, 0.4)
            print("  ✅ Звук выбора в меню (мягкий)")

            self.sounds['menu_move'] = self.create_beep(330, 0.05, 0.3)
            print("  ✅ Звук навигации в меню (тихий)")

            print("🎵 Все звуки сгенерированы!")

            print("\n🔊 ТЕСТ ЗВУКОВ:")
            if 'flap' in self.sounds and self.sounds['flap']:
                print("Проигрываю тестовый звук взмаха (теперь мягкий)...")
                self.sounds['flap'].play()
                print("✅ Звук запущен!")

        except Exception as e:
            print(f"⚠️ Ошибка генерации звуков: {e}")
            import traceback
            traceback.print_exc()
            self.sound_enabled = False

    def play(self, sound_name):
        if not self.sound_enabled:
            return

        if sound_name in self.sounds and self.sounds[sound_name]:
            try:
                self.sounds[sound_name].play()
            except Exception as e:
                print(f"⚠️ Ошибка воспроизведения {sound_name}: {e}")

    def stop_all(self):
        try:
            pygame.mixer.stop()
        except:
            pass


_sound_generator = None


def get_sound_generator():
    global _sound_generator
    if _sound_generator is None:
        _sound_generator = SoundGenerator()
    return _sound_generator


def play_sound(sound_name):
    generator = get_sound_generator()
    if generator:
        generator.play(sound_name)
