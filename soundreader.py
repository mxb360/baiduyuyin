from aip import AipSpeech
import pygame
import time


def aipSpeech(text, name):
    print('正在尝识别文字：\n" ' + text + ' "')

    app_id = "10541118"
    api_key = "b0LxyNsshrFd3fG6mO4scThn"
    secret_key = "u8kSnDhKydpAoatXMa8NIwYrolQOYyHy"
    client = AipSpeech(app_id, api_key, secret_key)
    result = client.synthesis(text, 'zh', 1, {'vol': 5})

    if isinstance(result, dict):
        print("语音合成失败！")
        return result
    else:
        print("语音合成成功！")
        with open(name, 'wb') as f:
            f.write(result)

        print("生成文件：", name)
        return "succeed"


def playwav(name):
    print("开始播放:", name.decode())
    pygame.mixer.init()
    music = pygame.mixer.music.load(name)
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.3)
    h = m = s = 0
    while pygame.mixer.music.get_busy():
        time.sleep(1)
        print("\r%02d:%02d:%02d"%(h, m, s), end="")
        s += 1
        if s == 60:
            m, s = m+1, 0
        if m == 60:
            h, m = h+1, 0
    print("\n" + name.decode(), "播放结束")

if __name__ == '__main__':
    import sys
    playwav(sys.argv[1].encode())
