# Asset manager to download, cache, and load design assets from the HTML templates
import os
import threading
import urllib.request

import pygame

ASSETS = {
    "mahogany_table": "https://lh3.googleusercontent.com/aida-public/AB6AXuCU7z0pfbgR5hgPgLjibdqjRhn6otjUuiBCD-7TPsZDbUrDoN1v5FFLjxns-oRAGXumqrkdGJUnYuZby4CWBueoeHSc0gtzmWvZbuASEnKIpM43Xj4ps8TUu5fjUsdyLlhrrAf6KKYLTrVeWGkMggTU34ua_neRzf-oCLyeiuJcBqPpNFY_9gOrm1GpcEQ7-XrJBaGCHB03p4oDc-__XusL-G3eNSuSSzFLSdqyeq7oKVFTNFxSJfmCtQXW7H_Of3AuovRq7vKHNWk",
    "board_parchment": "https://lh3.googleusercontent.com/aida-public/AB6AXuAexNqUxP2fcVe6i9rhuMPuX1zCBogluqxGjMK11zdvhsbdakc9S53y_MZMht0HmfcPlbnZlCHsyhOlUFPCbolZOxDIzNZxGpKL1semFZjLvsCg4swMt9z6RLsnEnam2U50fFoHX_C4E9v5M67Xhd6YTvC204jAqdL3q9mYrMYfvzMjubXmlo3m3l7skaCnv2Zepg0OU5esSNGqINjasDIRpAJoFCeT3mQvz0q9lxH2b79JQ6EkVfJTE6EbMNNXVX4a5Vw4ff21mH4",
    "board_marble": "https://lh3.googleusercontent.com/aida-public/AB6AXuCeeLffapQcsRaS1CgMO9JTu05BUfAaUWduIhiVVXdBig7OMKlMzHa-1Vnmf-xDljN3n3YNbli5YkkAmj-aiYBDtpiu9oxMQKimctREWX9v3shMUdfQuCvyTUZRbOjpAhCQ03Zd01UjguxVWK-LL2BTaQG31nC5MN45HoF_hYf-EZjTbM3jqVcuNqRq8wfBqY7duXIngRsN4b388tG9UKkvuPySUBt9Ar9RDfP4muzOH1NKRLpVzSnd2q1HlZcMMqg42cVN1gY4pfw",
    "board_glass": "https://lh3.googleusercontent.com/aida-public/AB6AXuBY4Z7U3ekc3xDfRJ0WsBYtINB9JFlCTlkl6Emx5Fccub0SwsIi7ZA0GTOkTVcl-5iAu3_OQdsIVfwVlSttI1f38bLgTdOF6zjOnQF_byygpQ96jigz8rrZp8LDJfj24T1Z6J58AHzndEzB5m1Vlr88vtnfN-nc4X36GBGDLh35Z_9r20svZECHmLfmORluI-qf2kSf4uz0JgZbI0LqoGqTmBBwj8va3T1Oy629cS3FcpidBRjiaq-f1X_yTX14ndEy8hJNBWBy5qo",
    "piece_jade": "https://lh3.googleusercontent.com/aida-public/AB6AXuDumaFKweac3AXrNdjpMvYxGiPkF-hzHgiw3tC0N6Om_8c6oLyFzU7exdG6qWSDMcBk8-fHbDFP8da8CTZ48KDtk0SRVQ6zHSTUHeCw-5udwDKsE369eGIVu81uyd_8Hc1DdznDxQRYnra-MEhCBoEG_SqaTuPgbCQ-86IKPHI3A1kGiXH_r1_8bSaI_PhcC97Wvre6JcK71B5NmnpS4uueMF04mA1jKEBu3t9q1lcjeILtdd5GLCvLH3mH_TASa1oTA0fFLNoXZ4M",
    "piece_steel": "https://lh3.googleusercontent.com/aida-public/AB6AXuDDFjw3UIgu4GronWcaAQ3izM7H7HdAJnsBF83upMcQxgKsjYt1zYLMpAyrA6gi5D_i4F_SeJS66QfiKoRkmr_t2xBG2oJf27ctQJu0kJqMEgYE15RyhYIp3UnUc4bWLaDI90AXif1KZw_JNX-TP_uitI8LJZyMaSq1d0gq0xysT9T_4HduSR9y4Zcn8nqDDHOmKteM2vEUv3RteZ395horlGjwSvRa_q39amrvOSxSYkD1VeKgIWv2oH4Db5mpEC1tSnswhWqxEro",
    "avatar_opponent": "https://lh3.googleusercontent.com/aida-public/AB6AXuCd2dyWl3KDjcQTXwiqrWxlCsz7fwi1aC-Bm74yP3lMCG18NnnMl20tx4OJ_BsmmBgfE-ZV3KVaCaSQ-h4DpghTeMWoLcND4iRTFStqbT437fZNbM-ASed-ct4VTLfhFe4t3_9h2m37mswr0gPqt7MD5J6CeRgwhVCfWTrrybpbO6W-U72UufBXez00jsKpl9zJM6nM-iNgRbeCbiAQZr89ZMpDrCTvnSTdISEv34eVKVcm5sZqV_yAHT_FiF0b3PBLD-mryTbuYYg",
    "avatar_player": "https://lh3.googleusercontent.com/aida-public/AB6AXuDNyMl3rUGH60T9G5I3OPiJdd4FjAKqwlg1BnolQbTqkAGDV7aMm7kIHJcqwkM7LvOqks9Hcwa3l5LzQ1Zb6Fqsk2CySqWiZaX5BJAIJdV_NQrmAVhoPjmUaG_L4OOdfgFEy8VASSGeYeADkEY1lMZ6koJeNly4_pDvAlBNUHiorBa94QpYZViJWNskhoA1h6vJEjqgmL90ixP5k2viMxP_bpvPNtiW0FPYM2rWzsgJaaprJh9h41fmkD56fDyBItaVuN-kBCXCFW4",
}

_cache = {}
_downloaded_count = 0
_lock = threading.Lock()


def start_preload():
    """Starts background thread to download assets asynchronously"""
    t = threading.Thread(target=_download_all)
    t.daemon = True
    t.start()


def _download_all():
    global _downloaded_count
    cache_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets_cache"
    )
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    for name, url in ASSETS.items():
        local_path = os.path.join(cache_dir, f"{name}.jpg")
        if not os.path.exists(local_path):
            try:
                # Custom user-agent to bypass basic scrape blocks
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                with (
                    urllib.request.urlopen(req) as response,  # nosec B310
                    open(local_path, "wb") as out_file,
                ):
                    out_file.write(response.read())
            except Exception as e:
                print(f"Error preloading asset {name}: {e}")

        # Load and cache
        try:
            img = pygame.image.load(local_path)
            with _lock:
                _cache[name] = img
                _downloaded_count += 1
        except Exception:
            pass


def get_asset(name):
    """Retrieves preloaded image, or loads from disk, or returns None if unavailable"""
    with _lock:
        if name in _cache:
            return _cache[name]

    if name == "custom_board":
        custom_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "image_readme",
            "image.png",
        )
        if os.path.exists(custom_path):
            try:
                img = pygame.image.load(custom_path)
                with _lock:
                    _cache[name] = img
                return img
            except Exception as e:
                print(f"Error loading custom board: {e}")

    cache_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets_cache"
    )
    local_path = os.path.join(cache_dir, f"{name}.jpg")
    if os.path.exists(local_path):
        try:
            img = pygame.image.load(local_path)
            with _lock:
                _cache[name] = img
            return img
        except Exception:
            pass
    return None
