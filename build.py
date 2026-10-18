"""Build the public static site; no dependencies, credentials, analytics or backend."""
from pathlib import Path
import json, html, shutil, re

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'dist'
if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir()
shutil.copytree(ROOT / 'assets', OUT / 'assets')

DATA = json.loads((ROOT / 'content.json').read_text(encoding='utf-8'))
BASE = 'https://dvk.vn'

def esc(s):
    return html.escape(str(s), quote=True)

def url(path, lang):
    return ('/vi' if lang == 'vi' else '') + path

PATHS = {
    'home': '/',
    'catalog': '/games/',
    'siteprivacy': '/privacy/',
    'support': '/support/',
    'game': '/puzzle-spark/',
    'privacy': '/puzzle-spark/privacy/',
    'terms': '/puzzle-spark/terms/',
    'block_game': '/block-puzzle/',
    'block_privacy': '/block-puzzle/privacy/',
    'block_terms': '/block-puzzle/terms/',
}

SEO = {
    'en': {
        'home': ('Block Puzzle 8x8: Neon Master — Official Game & Studio Showcase | DVK', 'Discover Block Puzzle 8x8: Neon Master. 8 candy-neon game modes, 20 Story Saga stages, online live events, tactical boosters, combo mechanics, and pure offline play on iOS and Android.'),
        'catalog': ('Games by DVK — Block Puzzle 8x8: Neon Master & Puzzle Spark', 'Explore indie mobile games by DVK. Meet Block Puzzle 8x8: Neon Master with 8 modes and Story Saga, and Puzzle Spark with 240 logic puzzles.'),
        'siteprivacy': ('DVK Website Privacy Policy', 'Learn about privacy on dvk.vn, website hosting and game data handling policies.'),
        'support': ('DVK Support — Game Help & Bug Reports', 'Get direct support for Block Puzzle 8x8: Neon Master and Puzzle Spark. Contact game@dvk.vn.'),
        'game': ('Puzzle Spark — Lights Out Logic Puzzle | DVK', 'Explore Puzzle Spark: 240 Lights Out puzzles across 24 difficulty tiers, daily challenges, hints and five languages.'),
        'privacy': ('Puzzle Spark Privacy Policy | DVK', 'Read how the Puzzle Spark preview handles local progress, reminders, and advertising.'),
        'terms': ('Puzzle Spark Terms of Use | DVK', 'Terms of use for the Puzzle Spark preview: game progress, hints, and support.'),
        'block_game': ('Block Puzzle 8x8: Neon Master — Classic Grid, Story Saga & Combos | DVK', 'Master the 8x8 neon grid! 8 candy-neon modes, 20 Story Saga stages, online live events, tactical boosters, combo streaks, and pure offline play on iOS and Android.'),
        'block_privacy': ('Block Puzzle 8x8 Privacy Policy | DVK', 'Official privacy policy for Block Puzzle 8x8: Neon Master. Details on on-device data storage, in-app purchases, and Google AdMob integration.'),
        'block_terms': ('Block Puzzle 8x8 Terms of Use | DVK', 'Official terms of use for Block Puzzle 8x8: Neon Master. Rules on virtual coins, boosters, permanent No-Ads package, and fair play.'),
    },
    'vi': {
        'home': ('Block Puzzle 8x8: Neon Master — Game Xếp Hình 8x8 & Cốt Truyện | DVK', 'Khám phá Block Puzzle 8x8: Neon Master. 8 chế độ game kẹo neon đỉnh cao, 20 ải Cốt truyện, giải đấu trực tuyến, bảo bối cứu nguy, hướng dẫn chơi và chế độ offline 100% trên iOS & Android.'),
        'catalog': ('Trò Chơi Từ DVK — Block Puzzle 8x8 & Puzzle Spark', 'Bộ sưu tập game di động độc lập từ DVK: Trải nghiệm xếp hình Block Puzzle 8x8 phong cách neon và giải đố trí tuệ Puzzle Spark.'),
        'siteprivacy': ('Quyền riêng tư website DVK', 'Tìm hiểu quyền riêng tư trên dvk.vn, dịch vụ lưu trữ website và chính sách bảo mật ứng dụng.'),
        'support': ('Hỗ trợ DVK — Trợ giúp Game & Báo Lỗi', 'Nhận trợ giúp trực tiếp cho Block Puzzle 8x8: Neon Master và Puzzle Spark. Liên hệ email game@dvk.vn.'),
        'game': ('Puzzle Spark — Game giải đố Lights Out | DVK', 'Khám phá 240 màn Lights Out qua 24 tầng khó, thử thách hằng ngày và gợi ý trong Puzzle Spark.'),
        'privacy': ('Quyền riêng tư Puzzle Spark | DVK', 'Thông tin dữ liệu của bản thử nghiệm Puzzle Spark: tiến độ trên thiết bị, nhắc nhở và quảng cáo.'),
        'terms': ('Điều khoản Puzzle Spark | DVK', 'Điều khoản sử dụng bản thử nghiệm Puzzle Spark, gồm tiến độ, gợi ý và hỗ trợ.'),
        'block_game': ('Block Puzzle 8x8: Neon Master — Hướng Dẫn & Tính Năng Đỉnh Cao | DVK', 'Game xếp hình 8x8 đỉnh cao phong cách neon rực rỡ! 8 chế độ game, 20 ải Cốt truyện, giải đấu trực tuyến, bảo bối cứu nguy, chơi offline 100% không cần mạng.'),
        'block_privacy': ('Chính sách Quyền riêng tư Block Puzzle 8x8 | DVK', 'Chính sách bảo mật chính thức cho Block Puzzle 8x8: Neon Master: Lưu trữ tiến độ cục bộ, thanh toán IAP an toàn, quảng cáo thân thiện.'),
        'block_terms': ('Điều khoản Sử dụng Block Puzzle 8x8 | DVK', 'Điều khoản sử dụng Block Puzzle 8x8: Neon Master: Quy định xu vàng, bảo bối cứu nguy, gói gỡ quảng cáo vĩnh viễn và hỗ trợ người chơi.'),
    }
}

TEXT = {
    'en': {
        'nav': ['Games', 'Privacy', 'Support'],
        'lang': 'Tiếng Việt',
        'terms': 'Terms',
        'privacy': 'Privacy',
        'support': 'Support',
        'contact': 'Get in touch',
        'foot': 'Crafted with care. Focused gameplay for every moment.',
        'provider': 'Developer brand: DVKapp. Support: game@dvk.vn.',
        'webtitle': 'About this website',
        'webbody': 'This website has no account, contact form, advertising SDK, analytics script or tracking cookie. Email opens your own mail app. Hosted on GitHub Pages and managed through Cloudflare.',
        'notmoney': 'Coins, stars and trophies are in-game virtual assets and cannot be exchanged for cash.',
        'supporttitle': 'Direct Developer Support',
        'supportlead': 'Have questions, found a bug, or want to share feedback? Reach out to DVKapp directly.',
        'email': 'Email support',
        'reporttitle': 'Help us reproduce an issue',
        'report': 'Include your app version, device model, operating system and steps that led to the issue. Never send passwords or financial credentials.',
        'savedtitle': 'About your game progress',
        'saved': 'Your game progress is saved locally and securely on your device.',
        'notifytitle': 'Reminders are strictly optional',
        'notify': 'Local notification reminders can be toggled on or off inside the in-game Settings.',
        'legalnote': 'Official Policy · Updated 18 October 2026',
        'block_privacytitle': 'Block Puzzle 8x8 Privacy Policy',
        'block_privacylead': 'Clear, transparent privacy principles for Block Puzzle 8x8: Neon Master. No accounts, no personal tracking, and local progress storage.',
        'block_termstitle': 'Block Puzzle 8x8 Terms of Use',
        'block_termslead': 'Terms of use, virtual coins, IAP policies, and player guidelines for Block Puzzle 8x8: Neon Master.',
        'privacytitle': 'Your privacy, in plain words.',
        'privacylead': 'This policy describes the current Puzzle Spark preview and this website.',
        'termstitle': 'Terms of use',
        'termslead': 'The terms for the current Puzzle Spark preview.',
        'game_intro': 'Turn every light off. Each tap changes a cell and its edge-sharing neighbors. A simple rule, with room to think.',
        'status': 'Preview build · Store release in preparation',
        'explore': 'Discover Puzzle Spark',
        'gamelead': 'One rule. A whole journey.',
        'details': '240 unique puzzles, arranged into 24 tiers of 10. Start with 3×3, progress to 4×4 and 5×5.',
        'hints': 'Help, on your terms.',
        'hintbody': 'Two free daily hints and voluntary rewarded ads in development builds.',
        'five': 'Five languages. One spark.',
        'fivebody': 'English, Vietnamese, Spanish, Portuguese and Japanese available in Settings.',
        'how': 'Rules & How to Play',
        'gridlabel': 'Illustration of a Lights Out puzzle',
    },
    'vi': {
        'nav': ['Trò chơi', 'Quyền riêng tư', 'Hỗ trợ'],
        'lang': 'English',
        'terms': 'Điều khoản',
        'privacy': 'Quyền riêng tư',
        'support': 'Hỗ trợ',
        'contact': 'Liên hệ',
        'foot': 'Trò chơi nhỏ. Khoảng trời tập trung và sáng tạo.',
        'provider': 'Thương hiệu phát triển: DVKapp. Hỗ trợ: game@dvk.vn.',
        'webtitle': 'Về website này',
        'webbody': 'Website không có tài khoản, biểu mẫu liên hệ, SDK quảng cáo hay cookie theo dõi. Lưu trữ trên GitHub Pages và quản lý qua Cloudflare.',
        'notmoney': 'Xu vàng, bảo bối và cúp sao là thành tích trong trò chơi, không phải tiền hoặc hiện vật.',
        'supporttitle': 'Hỗ Trợ Trực Tiếp Từ Lập Trình Viên',
        'supportlead': 'Bạn có câu hỏi, gặp lỗi kỹ thuật hoặc có ý tưởng đóng góp? Hãy liên hệ trực tiếp với DVKapp.',
        'email': 'Hỗ trợ qua email',
        'reporttitle': 'Giúp chúng tôi tái hiện lỗi',
        'report': 'Gửi phiên bản app, dòng máy, hệ điều hành và các bước dẫn tới lỗi. Không gửi mật khẩu hay thông tin thanh toán.',
        'savedtitle': 'Về tiến độ đã lưu',
        'saved': 'Tiến độ được lưu an toàn trên thiết bị của bạn.',
        'notifytitle': 'Nhắc hẹn là tùy chọn',
        'notify': 'Bạn có thể bật hoặc tắt thông báo trong phần Cài đặt của game.',
        'legalnote': 'Chính sách chính thức · Cập nhật 18/10/2026',
        'block_privacytitle': 'Chính Sách Quyền Riêng Tư Block Puzzle 8x8',
        'block_privacylead': 'Quy định bảo mật minh bạch cho Block Puzzle 8x8: Neon Master. Không yêu cầu tài khoản, không theo dõi cá nhân, bảo mật giao dịch IAP tuyệt đối.',
        'block_termstitle': 'Điều Khoản Sử Dụng Block Puzzle 8x8',
        'block_termslead': 'Điều khoản sử dụng, quy định xu ảo, vật phẩm bảo bối và gói gỡ quảng cáo vĩnh viễn trong Block Puzzle 8x8: Neon Master.',
        'privacytitle': 'Quyền riêng tư, trình bày rõ ràng.',
        'privacylead': 'Chính sách mô tả bản thử nghiệm Puzzle Spark hiện tại và website này.',
        'termstitle': 'Điều khoản sử dụng',
        'termslead': 'Điều khoản dành cho bản thử nghiệm Puzzle Spark hiện tại.',
        'game_intro': 'Tắt hết các ô sáng. Mỗi lần chạm sẽ đổi trạng thái một ô và các ô chung cạnh.',
        'status': 'Bản thử nghiệm · Đang chuẩn bị phát hành',
        'explore': 'Khám phá Puzzle Spark',
        'gamelead': 'Một quy luật. Cả một hành trình.',
        'details': '240 bảng khác nhau, chia 24 tầng, mỗi tầng 10 màn. Bắt đầu với lưới 3×3, tiến tới 4×4 và 5×5.',
        'hints': 'Trợ giúp theo lựa chọn của bạn.',
        'hintbody': 'Mỗi ngày có hai gợi ý miễn phí và quảng cáo nhận thưởng tự nguyện trong bản phát triển.',
        'five': 'Năm ngôn ngữ. Chung một tia sáng.',
        'fivebody': 'Mặc định tiếng Anh; có thể chọn tiếng Việt, Tây Ban Nha, Bồ Đào Nha hoặc Nhật.',
        'how': 'Luật chơi & Kỹ năng',
        'gridlabel': 'Hình minh họa bảng giải đố Lights Out',
    }
}

def structured(kind, lang, canonical, title, desc):
    org = {
        '@type': 'Organization',
        '@id': BASE + '/#organization',
        'name': 'DVK',
        'url': BASE + '/',
        'email': 'game@dvk.vn',
        'logo': BASE + '/assets/dvk-mark.svg',
    }
    page = {
        '@type': 'WebPage',
        '@id': canonical + '#webpage',
        'url': canonical,
        'name': title,
        'description': desc,
        'inLanguage': lang,
        'isPartOf': {'@id': BASE + '/#website'},
    }
    graph = [
        org,
        {
            '@type': 'WebSite',
            '@id': BASE + '/#website',
            'url': BASE + '/',
            'name': 'DVK',
            'publisher': {'@id': BASE + '/#organization'},
        },
        page,
    ]

    if kind in ['home', 'block_game']:
        game = {
            '@type': 'VideoGame',
            '@id': BASE + '/block-puzzle/#game',
            'name': 'Block Puzzle 8x8: Neon Master',
            'url': BASE + '/block-puzzle/',
            'description': desc,
            'genre': 'Block Puzzle, Brain Training, Strategy, Casual',
            'gamePlatform': ['iOS', 'Android'],
            'inLanguage': ['en', 'vi'],
            'image': BASE + '/assets/block-puzzle-icon.png',
            'publisher': {'@id': BASE + '/#organization'},
            'applicationCategory': 'Game',
            'operatingSystem': 'iOS 15.0+, Android 8.0+',
        }
        graph.append(game)
        page['about'] = {'@id': game['@id']}
    elif kind == 'game':
        game = {
            '@type': 'VideoGame',
            '@id': BASE + '/puzzle-spark/#game',
            'name': 'Puzzle Spark',
            'url': canonical,
            'description': desc,
            'genre': 'Logic puzzle',
            'gamePlatform': 'Android',
            'inLanguage': ['en', 'vi', 'es', 'pt', 'ja'],
            'image': BASE + '/assets/puzzle-spark-icon.png',
            'publisher': {'@id': BASE + '/#organization'},
        }
        graph.append(game)
        page['about'] = {'@id': game['@id']}

    if kind in ['game', 'privacy', 'terms', 'catalog', 'block_game', 'block_privacy', 'block_terms']:
        parts = [('DVK', url('/', lang)), ('Trò chơi' if lang == 'vi' else 'Games', url(PATHS['catalog'], lang))]
        if 'block' in kind:
            parts.append(('Block Puzzle 8x8', url(PATHS['block_game'], lang)))
            if kind == 'block_privacy':
                parts.append((TEXT[lang]['privacy'], url(PATHS['block_privacy'], lang)))
            elif kind == 'block_terms':
                parts.append((TEXT[lang]['terms'], url(PATHS['block_terms'], lang)))
        elif kind != 'catalog':
            parts.append(('Puzzle Spark', url(PATHS['game'], lang)))
            if kind in ['privacy', 'terms']:
                parts.append((TEXT[lang][kind], url(PATHS[kind], lang)))
        graph.append({
            '@type': 'BreadcrumbList',
            'itemListElement': [
                {'@type': 'ListItem', 'position': i + 1, 'name': name, 'item': BASE + path}
                for i, (name, path) in enumerate(parts)
            ],
        })

    return '<script type="application/ld+json">' + json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False).replace('<', '\\u003c') + '</script>'

def paragraph(text):
    s = esc(text)
    for target in ['policies.google.com/privacy', 'policies.google.com/technologies/ads']:
        s = s.replace(target, f'<a href="https://{target}" rel="external">{target}</a>')
    return '<p>' + s + '</p>'

def grid(t):
    cells = ''.join('<span class="cell ' + ('lit' if i in [1, 3, 4, 5, 7] else '') + '">' + ('✦' if i == 4 else '') + '</span>' for i in range(9))
    return '<div class="puzzle-art" role="img" aria-label="' + esc(t['gridlabel']) + '"><div class="orbit orbit-one"></div><div class="orbit orbit-two"></div><div class="board">' + cells + '</div><span class="art-note">3 × 3 / LIGHTS OUT</span></div>'

def shell(kind, lang, body, title):
    t = TEXT[lang]
    path = PATHS[kind]
    theme = 'block-puzzle' if ('block' in kind or kind == 'home') else 'puzzle-spark' if kind in ['game', 'privacy', 'terms'] else 'dvk'
    other = 'vi' if lang == 'en' else 'en'
    canonical = BASE + url(path, lang)
    nav = ''.join(
        f'<a href="{url(PATHS["catalog"] if k == "catalog" else PATHS[k], lang)}"' + (' aria-current="page"' if (kind == k or (k == "catalog" and ("game" in kind))) else '') + '>' + esc(n) + '</a>'
        for k, n in zip(['catalog', 'siteprivacy', 'support'], [('Trò chơi' if lang == 'vi' else 'Games'), t['privacy'], t['support']])
    )
    footer = ''.join(
        f'<a href="{url(PATHS[k], lang)}">{esc(t["privacy"] if k == "siteprivacy" else t[k])}</a>'
        for k in ['siteprivacy', 'terms', 'support']
    )
    title, desc = SEO[lang][kind]
    schema = structured(kind, lang, canonical, title, desc)
    crumbs = ''
    if theme == 'block-puzzle' and kind != 'home':
        crumbs = '<nav class="breadcrumbs" aria-label="Breadcrumb"><a href="' + url('/', lang) + '">DVK</a><span>/</span><a href="' + url(PATHS['catalog'], lang) + '">' + ('Trò chơi' if lang == 'vi' else 'Games') + '</a><span>/</span>'
        crumbs += ('<span aria-current="page">Block Puzzle 8x8</span>' if kind == 'block_game' else '<a href="' + url(PATHS['block_game'], lang) + '">Block Puzzle 8x8</a><span>/</span><span aria-current="page">' + esc(t['privacy'] if 'privacy' in kind else t['terms']) + '</span>') + '</nav>'
    elif theme == 'puzzle-spark':
        crumbs = '<nav class="breadcrumbs" aria-label="Breadcrumb"><a href="' + url('/', lang) + '">DVK</a><span>/</span><a href="' + url(PATHS['catalog'], lang) + '">' + ('Trò chơi' if lang == 'vi' else 'Games') + '</a><span>/</span>'
        crumbs += ('<span aria-current="page">Puzzle Spark</span>' if kind == 'game' else '<a href="' + url(PATHS['game'], lang) + '">Puzzle Spark</a><span>/</span><span aria-current="page">' + esc(t[kind]) + '</span>') + '</nav>'

    logo = '/assets/block-puzzle-icon.png' if theme == 'block-puzzle' else '/assets/spark.svg' if theme == 'puzzle-spark' else '/assets/dvk-mark.svg'
    ogimage = '/assets/block-preview-home.png' if theme == 'block-puzzle' else '/assets/puzzle-spark-icon.png' if theme == 'puzzle-spark' else '/assets/dvk-mark.svg'
    theme_color = '#090d1a' if theme == 'block-puzzle' else '#173e30' if theme == 'puzzle-spark' else '#152642'

    return f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="google-site-verification" content="VCgA69MCS2iiEJBLr5-Sl772K8mIju2FWOCB73ZwFCE"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><meta name="theme-color" content="{theme_color}"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{canonical}"><link rel="alternate" hreflang="en" href="{BASE + path}"><link rel="alternate" hreflang="vi" href="{BASE + url(path, 'vi')}"><link rel="alternate" hreflang="x-default" href="{BASE + path}"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{canonical}"><meta property="og:type" content="website"><meta property="og:site_name" content="DVK"><meta property="og:locale" content="{'vi_VN' if lang == 'vi' else 'en_US'}"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(desc)}"><meta property="og:image" content="{BASE}{ogimage}"><link rel="icon" type="image/png" href="{logo}"><link rel="stylesheet" href="/assets/site.css">{schema}</head><body data-theme="{theme}"><a class="skip" href="#main">{'Skip to content' if lang == 'en' else 'Đến nội dung'}</a><header><a class="brand" href="{url('/', lang)}" aria-label="DVK home"><img src="/assets/dvk-mark.svg" alt="" width="34" height="34">DVK</a><nav aria-label="{'Main navigation' if lang == 'en' else 'Điều hướng chính'}">{nav}<a class="language" href="{url(path, other)}" lang="{other}" hreflang="{other}">{esc(t['lang'])}</a></nav></header><main id="main">{crumbs}{body}</main><footer><div><a class="brand" href="{url('/', lang)}">DVK</a><p>{esc(t['foot'])}</p><a href="mailto:game@dvk.vn">game@dvk.vn</a></div><div class="footer-links">{footer}</div><small>© 2026 DVK · Apps & Games</small></footer></body></html>'''

def home(lang):
    vi = lang == 'vi'

    # English Default Copy
    if not vi:
        hero = '''<section class="hero studio-hero" style="min-height: auto; padding: 60px 48px 40px;">
            <div class="hero-copy">
                <p class="eyebrow" style="color:#00e5ff;">✦ DVK STUDIOS · FLAGSHIP RELEASE</p>
                <h1 style="color:#ffffff; margin-bottom: 20px;">Block Puzzle 8×8:<br><span style="background: linear-gradient(135deg, #00e5ff 0%, #ff2a85 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Neon Master</span></h1>
                <p class="lead" style="color:#cbd5e1; font-size: 19px; line-height: 1.7; max-width: 620px;">
                    The ultimate candy-neon 8×8 block puzzle experience on iOS & Android. Master <strong>8 dynamic game modes</strong>, conquer <strong>20 Story Saga stages</strong>, ignite blazing combo multipliers, and enjoy <strong>100% pure offline play</strong> with zero Wi-Fi required.
                </p>
                <div class="specs-badge-list">
                    <span class="specs-badge">⚡ iOS App Store (v1.0.0)</span>
                    <span class="specs-badge">🤖 Google Play Store</span>
                    <span class="specs-badge">📴 100% Pure Offline</span>
                    <span class="specs-badge">👁️ ADA Colorblind Safe</span>
                    <span class="specs-badge">🔊 Dynamic Voice Announcer</span>
                </div>
                <div class="actions" style="margin-top: 10px;">
                    <a class="button" href="#modes" style="background: linear-gradient(135deg, #00e5ff 0%, #0077ff 100%); color: #000; font-weight: 800; font-size: 15px;">Explore 8 Game Modes ↘</a>
                    <a class="button" href="#how-to-play" style="background: #1e293b; color: #fff; font-weight: 700; font-size: 15px;">How to Play & Pro Tips →</a>
                </div>
            </div>
            <div class="block-art" style="padding: 10px;">
                <img src="/assets/block-preview-home.png" alt="Block Puzzle 8x8 Neon Master Home Screen" width="390" height="844" style="max-width: 320px; box-shadow: 0 20px 50px rgba(0,229,255,0.3); border: 2px solid rgba(0,229,255,0.4);">
            </div>
        </section>'''

        # Gallery Strip with real screenshots
        gallery = '''<section style="padding: 10px 48px 40px;">
            <div class="project-heading">
                <div>
                    <p class="eyebrow" style="color:#00e5ff;">OFFICIAL SCREENSHOTS</p>
                    <h2 style="color:#fff; margin: 4px 0 0;">Experience the Vibrant Neon Universe</h2>
                </div>
            </div>
            <div class="gallery-strip">
                <div class="gallery-card">
                    <img src="/assets/block-preview-home.png" alt="Candy Neon Home Menu" loading="lazy">
                    <div class="gallery-card-caption">Main Menu · 8 Modes</div>
                </div>
                <div class="gallery-card">
                    <img src="/assets/block-preview-gameplay.png" alt="8x8 Grid Gameplay & Combos" loading="lazy">
                    <div class="gallery-card-caption">8×8 Grid · Combo Blast</div>
                </div>
                <div class="gallery-card">
                    <img src="/assets/block-preview-story.png" alt="Story Saga Map 20 Stages" loading="lazy">
                    <div class="gallery-card-caption">Story Saga · 20 Stages</div>
                </div>
                <div class="gallery-card">
                    <img src="/assets/block-preview-events.png" alt="Online Live Events Tournament" loading="lazy">
                    <div class="gallery-card-caption">Live Events · Trophy Race</div>
                </div>
                <div class="gallery-card">
                    <img src="/assets/block-preview-quests.png" alt="Daily Quests and 21-Day Streak" loading="lazy">
                    <div class="gallery-card-caption">21-Day Streak & Quests</div>
                </div>
                <div class="gallery-card">
                    <img src="/assets/block-preview-tutorial.png" alt="How to Play Onboarding" loading="lazy">
                    <div class="gallery-card-caption">Interactive Guide</div>
                </div>
            </div>
        </section>'''

        # 8 Game Modes Full Grid
        modes = '''<section id="modes" style="padding: 20px 48px 50px;">
            <div class="project-heading">
                <div>
                    <p class="eyebrow" style="color:#00e5ff;">8 DIVERSE GAME MODES</p>
                    <h2 style="color:#fff; margin: 4px 0 0;">Tailored for Every Puzzle Mood</h2>
                </div>
            </div>
            <div class="modes-grid">
                <article class="mode-card">
                    <div class="mode-card-header">
                        <span class="mode-card-icon">🎮</span>
                        <span class="mode-badge" style="background:#0284c7;">GO!</span>
                    </div>
                    <div>
                        <h3>1. Classic Endless Play</h3>
                        <p>The quintessential 8×8 block puzzle experience. Zero stressful timers, zero energy limits. Place shapes, clear horizontal and vertical lines, trigger multipliers, and chase personal high-score records at your own comfortable pace.</p>
                    </div>
                </article>

                <article class="mode-card">
                    <div class="mode-card-header">
                        <span class="mode-card-icon">📖</span>
                        <span class="mode-badge" style="background:#7c3aed;">★ 0-60 STARS</span>
                    </div>
                    <div>
                        <h3>2. Story Saga (20 Stages)</h3>
                        <p>An epic 4-chapter narrative campaign! Clear line quotas, conquer move-limited puzzles, and outsmart intense Boss stages. Earn up to 3 stars per stage and unlock the breathtaking Galaxy visual theme upon conquering Chapter 1.</p>
                    </div>
                </article>

                <article class="mode-card">
                    <div class="mode-card-header">
                        <span class="mode-card-icon">🔥</span>
                        <span class="mode-badge" style="background:#ea580c;">LIVE NOW</span>
                    </div>
                    <div>
                        <h3>3. Online Live Events</h3>
                        <p>Limited-time Grand Prix tournaments! Rack up trophies with multi-line clears and combo streaks. Climb the live leaderboard ladder against worldwide challengers and claim exclusive milestone chests and VIP cosmetics.</p>
                    </div>
                </article>

                <article class="mode-card">
                    <div class="mode-card-header">
                        <span class="mode-card-icon">📅</span>
                        <span class="mode-badge" style="background:#059669;">🏆 31D CUP</span>
                    </div>
                    <div>
                        <h3>4. Monthly Calendar Challenge</h3>
                        <p>A fresh puzzle challenge every day of the month! Unlock daily calendar dates sequentially, sharpen your daily problem solving, and collect the Bronze Cup, Silver Cup, and prestigious Gold Master Trophy.</p>
                    </div>
                </article>

                <article class="mode-card">
                    <div class="mode-card-header">
                        <span class="mode-card-icon">🎁</span>
                        <span class="mode-badge" style="background:#e11d48;">CLAIM COINS</span>
                    </div>
                    <div>
                        <h3>5. Daily Quests & 21-Day Streak</h3>
                        <p>Cultivate a rewarding daily habit. Complete 5 daily missions (clearing specific shapes, triggering combos, achieving milestone points) and maintain a 21-day login streak to unlock massive gold coin rewards.</p>
                    </div>
                </article>

                <article class="mode-card">
                    <div class="mode-card-header">
                        <span class="mode-card-icon">👑</span>
                        <span class="mode-badge" style="background:#b45309;">TOP 50</span>
                    </div>
                    <div>
                        <h3>6. Global Leaderboard</h3>
                        <p>Ascend the ranks from Novice and Warrior all the way to Apex Grandmaster and Legend. Compare your all-time highest scores with puzzle tacticians across the globe with custom gamer tags.</p>
                    </div>
                </article>

                <article class="mode-card">
                    <div class="mode-card-header">
                        <span class="mode-card-icon">💎</span>
                        <span class="mode-badge" style="background:#4338ca;">VIP</span>
                    </div>
                    <div>
                        <h3>7. Item Shop & Visual Themes</h3>
                        <p>Personalize your 8×8 grid with premium aesthetics: Classic Neon, Deep Galaxy, Cyberpunk, Emerald Forest, and Sunset Gold. Refill emergency boosters or unlock the permanent Remove Ads package with one tap.</p>
                    </div>
                </article>

                <article class="mode-card">
                    <div class="mode-card-header">
                        <span class="mode-card-icon">💡</span>
                        <span class="mode-badge" style="background:#0f766e;">PRO TIPS</span>
                    </div>
                    <div>
                        <h3>8. Interactive Master Tutorial</h3>
                        <p>A detailed 5-slide visual tutorial explaining board spatial management, central 3×3 clearance, multi-line blast mechanics, and combo stacking strategies to help beginners become puzzle grandmasters.</p>
                    </div>
                </article>
            </div>
        </section>'''

        # Tactical Boosters Section
        boosters = '''<section style="padding: 10px 48px 45px;">
            <div class="project-heading">
                <div>
                    <p class="eyebrow" style="color:#00e5ff;">TACTICAL ARSENAL</p>
                    <h2 style="color:#fff; margin: 4px 0 0;">4 Smart Power-Up Boosters</h2>
                </div>
            </div>
            <p style="color:#94a3b8; font-size: 16px; max-width: 700px; margin-top: 8px;">
                Never feel trapped by awkward shapes. Turn difficult board jams into triumphant combo chains with our balanced tactical power-up system.
            </p>
            <div class="boosters-grid">
                <div class="booster-card">
                    <strong><span>🔄</span> ROTATE BOOSTER</strong>
                    <p>Rotate any block in your bottom tray by 90 degrees. Turn an awkward 3-block L or bar piece into the exact shape needed to slide into tight spaces.</p>
                </div>
                <div class="booster-card">
                    <strong><span>↩️</span> UNDO BOOSTER</strong>
                    <p>Made an accidental drop or miscalculated your board space? Rewind your previous move immediately with zero score penalty or progress loss.</p>
                </div>
                <div class="booster-card">
                    <strong><span>🔨</span> HAMMER 3×3</strong>
                    <p>Danger strikes when the board gets crowded! Shatter a congested 3×3 area anywhere on the grid to create breathing room and save your run.</p>
                </div>
                <div class="booster-card">
                    <strong><span>👁️</span> NEXT QUEUE PREVIEW</strong>
                    <p>Unlock the ability to peek at the next 3 incoming shapes before they hit the tray. Plan 2-3 moves ahead to engineer massive multi-line chain reactions!</p>
                </div>
            </div>
        </section>'''

        # Step by Step How to Play & Combo Mechanics Guide
        mechanics = '''<section id="how-to-play" class="mechanics-section" style="margin: 20px 48px 50px;">
            <p class="eyebrow" style="color:#00e5ff;">MASTER THE MECHANICS</p>
            <h2 style="color:#fff; margin: 4px 0 0;">How to Play & Score Multiplier Guide</h2>
            <p style="color:#cbd5e1; font-size: 16px; max-width: 720px; margin-top: 8px;">
                Follow these core tactical principles to climb the global leaderboard and achieve 5,000+ points in every run.
            </p>
            <div class="mechanics-grid">
                <div class="step-item">
                    <span class="step-number">STEP 01</span>
                    <h4>Drag & Place Blocks</h4>
                    <p>Pick one of the 3 available neon blocks from your tray and drag it onto empty cells on the 8×8 grid. Once placed, blocks cannot be moved except with the Undo tool.</p>
                </div>
                <div class="step-item">
                    <span class="step-number">STEP 02</span>
                    <h4>Line Blast Clears</h4>
                    <p>Fill an entire horizontal row (8 cells) or vertical column (8 cells) to vaporize all blocks in that line. Cleared space is instantly available for upcoming pieces.</p>
                </div>
                <div class="step-item">
                    <span class="step-number">STEP 03</span>
                    <h4>Multi-Line Bonuses</h4>
                    <p>Clear 2, 3, or 4 lines simultaneously in a single placement to earn exponential multi-clear bonus points: 2 lines (+20 pts), 3 lines (+40 pts), 4 lines (+80 pts)!</p>
                </div>
                <div class="step-item">
                    <span class="step-number">STEP 04</span>
                    <h4>Consecutive Combo Streaks</h4>
                    <p>Clear at least one line on consecutive turns to build a Combo streak! Multipliers scale from Combo x2 up to x10+ with electrifying English announcer cheers: <em>"Good!", "Great!", "Super Combo!", "Unbelievable!"</em></p>
                </div>
                <div class="step-item">
                    <span class="step-number">STEP 05</span>
                    <h4>The Golden 3×3 Safe Zone</h4>
                    <p><strong>Pro Strategy:</strong> Always maintain an open 3×3 square near the center of the board. This prevents sudden large square blocks from causing an unavoidable game over!</p>
                </div>
                <div class="step-item">
                    <span class="step-number">STEP 06</span>
                    <h4>100% Offline & Accessible</h4>
                    <p>Zero internet connection required. Features a dedicated ADA Colorblind Mode with distinct geometric symbols on blocks, ensuring comfortable play for everyone.</p>
                </div>
            </div>
            <div style="margin-top: 36px; padding-top: 24px; border-top: 1px solid rgba(255,255,255,0.15); display: flex; gap: 16px; align-items: center; flex-wrap: wrap;">
                <a class="button" href="/block-puzzle/privacy/" style="background:#00e5ff; color:#000; font-weight:800;">View Privacy Policy →</a>
                <a class="button" href="/block-puzzle/terms/" style="background:#1e293b; color:#fff; font-weight:700;">Terms of Use →</a>
                <a class="text-link" href="mailto:game@dvk.vn" style="color:#00e5ff;">Need Support? Contact game@dvk.vn →</a>
            </div>
        </section>'''

        # Indie Catalog Section (Puzzle Spark)
        spark = f'''<section id="catalog" style="padding: 20px 48px 50px;">
            <div class="project-heading">
                <div>
                    <p class="eyebrow" style="color:var(--muted);">DVK INDIE CATALOG</p>
                    <h2 style="color:#fff; margin: 4px 0 0;">More Games from DVK</h2>
                </div>
            </div>
            <article class="project-card" data-game="puzzle-spark" style="margin-top: 24px;">
                <div class="project-copy">
                    <div class="project-identity">
                        <img src="/assets/puzzle-spark-icon.png" width="72" height="72" alt="Puzzle Spark Icon">
                        <div>
                            <span class="project-index">02 / LOGIC PUZZLE</span>
                            <h3>Puzzle Spark</h3>
                        </div>
                    </div>
                    <p>A tranquil Lights Out logic puzzle. Turn every light off across 240 handcrafted stages with no timer pressure. Five languages and daily challenges.</p>
                    <div class="project-facts">
                        <span>240 puzzles</span>
                        <span>24 difficulty tiers</span>
                        <span>5 languages</span>
                    </div>
                    <div style="display:flex;gap:14px;align-items:center;flex-wrap:wrap;">
                        <a class="button" href="{url(PATHS['game'], lang)}" style="background:#173e30; color:#fff;">Discover Puzzle Spark ↗</a>
                        <a class="text-link" href="{url(PATHS['privacy'], lang)}" style="color:#616f65;">Privacy Policy →</a>
                    </div>
                </div>
                {grid(TEXT['en'])}
            </article>
        </section>'''

        return hero + gallery + modes + boosters + mechanics + spark

    # Vietnamese Copy
    else:
        hero = '''<section class="hero studio-hero" style="min-height: auto; padding: 60px 48px 40px;">
            <div class="hero-copy">
                <p class="eyebrow" style="color:#00e5ff;">✦ DVK STUDIOS · BẢN PHÁT HÀNH CHÍNH THỨC</p>
                <h1 style="color:#ffffff; margin-bottom: 20px;">Block Puzzle 8×8:<br><span style="background: linear-gradient(135deg, #00e5ff 0%, #ff2a85 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Neon Master</span></h1>
                <p class="lead" style="color:#cbd5e1; font-size: 19px; line-height: 1.7; max-width: 620px;">
                    Trò chơi xếp hình 8×8 phong cách neon kẹo ngọt đỉnh cao trên iOS & Android. Thỏa sức trải nghiệm <strong>8 chế độ game phong phú</strong>, chinh phục <strong>20 ải Cốt truyện</strong>, kích hoạt chuỗi Combo bão điểm và chơi <strong>offline 100%</strong> không cần Wi-Fi hay 4G.
                </p>
                <div class="specs-badge-list">
                    <span class="specs-badge">⚡ iOS App Store (v1.0.0)</span>
                    <span class="specs-badge">🤖 Google Play Store</span>
                    <span class="specs-badge">📴 Chơi Offline 100%</span>
                    <span class="specs-badge">👁️ Trợ Năng Mù Màu ADA</span>
                    <span class="specs-badge">🔊 Âm Thanh Cổ Vũ Sôi Động</span>
                </div>
                <div class="actions" style="margin-top: 10px;">
                    <a class="button" href="#modes" style="background: linear-gradient(135deg, #00e5ff 0%, #0077ff 100%); color: #000; font-weight: 800; font-size: 15px;">Khám Phá 8 Chế Độ Chơi ↘</a>
                    <a class="button" href="#how-to-play" style="background: #1e293b; color: #fff; font-weight: 700; font-size: 15px;">Hướng Dẫn Chơi & Mẹo Hay →</a>
                </div>
            </div>
            <div class="block-art" style="padding: 10px;">
                <img src="/assets/block-preview-home.png" alt="Block Puzzle 8x8 Neon Master Giao diện chính" width="390" height="844" style="max-width: 320px; box-shadow: 0 20px 50px rgba(0,229,255,0.3); border: 2px solid rgba(0,229,255,0.4);">
            </div>
        </section>'''

        gallery = '''<section style="padding: 10px 48px 40px;">
            <div class="project-heading">
                <div>
                    <p class="eyebrow" style="color:#00e5ff;">HÌNH ẢNH THỰC TẾ TRONG GAME</p>
                    <h2 style="color:#fff; margin: 4px 0 0;">Giao Diện Neon Đầy Sắc Màu & Đẳng Cấp</h2>
                </div>
            </div>
            <div class="gallery-strip">
                <div class="gallery-card">
                    <img src="/assets/block-preview-home.png" alt="Trang chủ 8 chế độ game" loading="lazy">
                    <div class="gallery-card-caption">Trang Chủ · 8 Chế Độ</div>
                </div>
                <div class="gallery-card">
                    <img src="/assets/block-preview-gameplay.png" alt="Lưới 8x8 và Combo" loading="lazy">
                    <div class="gallery-card-caption">Lưới 8×8 · Bão Combo</div>
                </div>
                <div class="gallery-card">
                    <img src="/assets/block-preview-story.png" alt="Bản đồ 20 ải Cốt truyện" loading="lazy">
                    <div class="gallery-card-caption">Cốt Truyện · 20 Ải</div>
                </div>
                <div class="gallery-card">
                    <img src="/assets/block-preview-events.png" alt="Sự kiện trực tuyến đua cúp" loading="lazy">
                    <div class="gallery-card-caption">Sự Kiện · Đua Cúp VIP</div>
                </div>
                <div class="gallery-card">
                    <img src="/assets/block-preview-quests.png" alt="Điểm danh 21 ngày và nhiệm vụ" loading="lazy">
                    <div class="gallery-card-caption">Điểm Danh 21 Ngày</div>
                </div>
                <div class="gallery-card">
                    <img src="/assets/block-preview-tutorial.png" alt="Hướng dẫn kỹ năng chơi" loading="lazy">
                    <div class="gallery-card-caption">Hướng Dẫn 5 Bước</div>
                </div>
            </div>
        </section>'''

        modes = '''<section id="modes" style="padding: 20px 48px 50px;">
            <div class="project-heading">
                <div>
                    <p class="eyebrow" style="color:#00e5ff;">8 CHẾ ĐỘ CHƠI ĐỘC ĐÁO</p>
                    <h2 style="color:#fff; margin: 4px 0 0;">Phù Hợp Mọi Phong Cách & Mọi Lứa Tuổi</h2>
                </div>
            </div>
            <div class="modes-grid">
                <article class="mode-card">
                    <div class="mode-card-header">
                        <span class="mode-card-icon">🎮</span>
                        <span class="mode-badge" style="background:#0284c7;">GO!</span>
                    </div>
                    <div>
                        <h3>1. Chơi Cổ Điển Vô Tận (Classic Play)</h3>
                        <p>Trải nghiệm giải đố thuần túy và thư giãn tuyệt đối. Không giới hạn thời gian, không áp lực tim mạng. Kéo thả các khối hình, lấp đầy các hàng và cột để phá hủy và xác lập kỷ lục điểm số cá nhân mới.</p>
                    </div>
                </article>

                <article class="mode-card">
                    <div class="mode-card-header">
                        <span class="mode-card-icon">📖</span>
                        <span class="mode-badge" style="background:#7c3aed;">★ 0-60 SAO</span>
                    </div>
                    <div>
                        <h3>2. Cốt Truyện Saga (20 Ải Thử Thách)</h3>
                        <p>Hành trình thám hiểm qua 4 chương truyện hấp dẫn! Vượt qua chỉ tiêu phá dòng, giải đố trong số lượt đi giới hạn và đánh bại các ải Trùm cam go để săn 3 sao và mở khóa giao diện Galaxy tuyệt mỹ.</p>
                    </div>
                </article>

                <article class="mode-card">
                    <div class="mode-card-header">
                        <span class="mode-card-icon">🔥</span>
                        <span class="mode-badge" style="background:#ea580c;">ĐANG DIỄN RA</span>
                    </div>
                    <div>
                        <h3>3. Sự Kiện Trực Tuyến (Online Live Events)</h3>
                        <p>Giải đấu Grand Prix giới hạn thời gian! Tích lũy Cúp vàng qua các pha phá dòng và chuỗi Combo, cạnh tranh thứ hạng trực tiếp trên bảng vàng và nhận rương phần thưởng cùng vật phẩm VIP độc quyền.</p>
                    </div>
                </article>

                <article class="mode-card">
                    <div class="mode-card-header">
                        <span class="mode-card-icon">📅</span>
                        <span class="mode-badge" style="background:#059669;">🏆 CÚP 31D</span>
                    </div>
                    <div>
                        <h3>4. Thử Thách Lịch Tháng (Monthly Challenge)</h3>
                        <p>Mỗi ngày trong tháng là một câu đố tư duy mới. Hoàn thành tuần tự các ngày để nhận Cúp Đồng, Cúp Bạc và chinh phục Cúp Vàng danh giá nhất tháng.</p>
                    </div>
                </article>

                <article class="mode-card">
                    <div class="mode-card-header">
                        <span class="mode-card-icon">🎁</span>
                        <span class="mode-badge" style="background:#e11d48;">NHẬN THƯỞNG</span>
                    </div>
                    <div>
                        <h3>5. Nhiệm Vụ Hằng Ngày & Điểm Danh 21 Ngày</h3>
                        <p>Rèn luyện thói quen tư duy mỗi ngày với 5 nhiệm vụ đa dạng (đặt khối, nổ dòng, tích điểm, dùng bảo bối) và chuỗi điểm danh 21 ngày với số xu thưởng lũy tiến cực kỳ giá trị.</p>
                    </div>
                </article>

                <article class="mode-card">
                    <div class="mode-card-header">
                        <span class="mode-card-icon">👑</span>
                        <span class="mode-badge" style="background:#b45309;">TOP 50</span>
                    </div>
                    <div>
                        <h3>6. Bảng Xếp Hạng Toàn Cầu (Leaderboards)</h3>
                        <p>Thăng cấp danh vọng từ Tập Sự, Chiến Binh lên Bậc Thầy và Bất Bại Apex Grandmaster. So tài trí tuệ cùng cộng đồng người chơi quốc tế với Gamer Tag cá nhân hóa.</p>
                    </div>
                </article>

                <article class="mode-card">
                    <div class="mode-card-header">
                        <span class="mode-card-icon">💎</span>
                        <span class="mode-badge" style="background:#4338ca;">VIP</span>
                    </div>
                    <div>
                        <h3>7. Cửa Hàng Vật Phẩm & Giao Diện (Shop)</h3>
                        <p>Tùy biến bảng cờ với bộ sưu tập giao diện đỉnh cao: Neon Cổ Điển, Vũ Trụ Galaxy, Cyberpunk, Rừng Ngọc Lục Bảo và Hoàng Hôn Vàng. Nạp thêm xu hoặc mua gói Gỡ Quảng Cáo vĩnh viễn.</p>
                    </div>
                </article>

                <article class="mode-card">
                    <div class="mode-card-header">
                        <span class="mode-card-icon">💡</span>
                        <span class="mode-badge" style="background:#0f766e;">MẸO CAO THỦ</span>
                    </div>
                    <div>
                        <h3>8. Hướng Dẫn Chơi Chi Tiết (Tutorial)</h3>
                        <p>Cẩm nang 5 slide sinh động hướng dẫn cách kiểm soát không gian bàn cờ, bảo toàn vùng 3×3 trung tâm, xếp chồng combo và chiến thuật đạt trên 5,000 điểm.</p>
                    </div>
                </article>
            </div>
        </section>'''

        boosters = '''<section style="padding: 10px 48px 45px;">
            <div class="project-heading">
                <div>
                    <p class="eyebrow" style="color:#00e5ff;">BẢO BỐI CHIẾN THUẬT</p>
                    <h2 style="color:#fff; margin: 4px 0 0;">Bộ 4 Công Cụ Cứu Nguy Thông Minh</h2>
                </div>
            </div>
            <p style="color:#94a3b8; font-size: 16px; max-width: 700px; margin-top: 8px;">
                Không bao giờ lo bị kẹt bàn cờ vì những khối hình khó. Tận dụng bộ bảo bối thông minh để biến thế cờ hiểm nghèo thành những pha bão combo ngoạn mục.
            </p>
            <div class="boosters-grid">
                <div class="booster-card">
                    <strong><span>🔄</span> ĐỔI CHIỀU (ROTATE)</strong>
                    <p>Xoay khối hình trong khay 90 độ theo chiều kim đồng hồ. Dễ dàng biến khối chữ L hoặc thanh dài thành hình dáng hoàn hảo để đặt vừa góc hẹp.</p>
                </div>
                <div class="booster-card">
                    <strong><span>↩️</span> HOÀN TÁC (UNDO)</strong>
                    <p>Lỡ tay đặt nhầm vị trí hoặc tính toán sai nước đi? Dùng Hoàn tác để quay lại nước cờ trước ngay lập tức mà không bị trừ điểm hay mất lượt.</p>
                </div>
                <div class="booster-card">
                    <strong><span>🔨</span> BÚA PHÁ HỦY (HAMMER 3×3)</strong>
                    <p>Nguy cấp khi bàn cờ quá chật chội! Kích hoạt Búa để nổ tung vùng 3×3 nghẹt thở ở bất kỳ vị trí nào, giải phóng khoảng trống vàng để tiếp tục ván đấu.</p>
                </div>
                <div class="booster-card">
                    <strong><span>👁️</span> XEM TRƯỚC 3 KHỐI TIẾP THEO</strong>
                    <p>Mở ẩn khay xem trước 3 khối sắp xuất hiện. Tính toán nước cờ trước 2-3 lượt đi để kiến tạo những pha nổ multi-line combo đỉnh cao!</p>
                </div>
            </div>
        </section>'''

        mechanics = '''<section id="how-to-play" class="mechanics-section" style="margin: 20px 48px 50px;">
            <p class="eyebrow" style="color:#00e5ff;">QUY LUẬT & KỸ NĂNG</p>
            <h2 style="color:#fff; margin: 4px 0 0;">Hướng Dẫn Cách Chơi & Cơ Chế Nhân Điểm Combo</h2>
            <p style="color:#cbd5e1; font-size: 16px; max-width: 720px; margin-top: 8px;">
                Nắm vững 6 nguyên tắc cốt lõi dưới đây để chinh phục bảng xếp hạng toàn cầu và dễ dàng đạt trên 5,000 điểm mỗi ván đấu.
            </p>
            <div class="mechanics-grid">
                <div class="step-item">
                    <span class="step-number">BƯỚC 01</span>
                    <h4>Kéo Thả Khối Vào Bảng</h4>
                    <p>Chọn 1 trong 3 khối hình neon có sẵn trong khay và kéo thả vào các ô trống trên lưới 8×8. Khối khi đã đặt sẽ cố định vị trí (trừ khi dùng Hoàn Tác).</p>
                </div>
                <div class="step-item">
                    <span class="step-number">BƯỚC 02</span>
                    <h4>Phá Hủy Hàng Ngang & Cột Dọc</h4>
                    <p>Lấp đầy một hàng ngang (8 ô) hoặc một cột dọc (8 ô) để làm biến mất các khối trên đường đó, giải phóng không gian bàn cờ cho các lượt đi kế tiếp.</p>
                </div>
                <div class="step-item">
                    <span class="step-number">BƯỚC 03</span>
                    <h4>Điểm Thưởng Nổ Đa Dòng (Multi-Line)</h4>
                    <p>Phá hủy cùng lúc 2, 3 hoặc 4 hàng/cột trong duy nhất một nước đi để nhận thưởng bùng nổ: 2 dòng (+20 điểm), 3 dòng (+40 điểm), 4 dòng (+80 điểm)!</p>
                </div>
                <div class="step-item">
                    <span class="step-number">BƯỚC 04</span>
                    <h4>Chuỗi Combo Bão Điểm Liên Hoàn</h4>
                    <p>Phá hủy ít nhất một dòng ở các nước đi liên tiếp nhau để kích hoạt chuỗi Combo! Điểm nhân tăng vọt từ Combo x2 lên tới x10+ cùng tiếng cổ vũ tiếng Anh sống động: <em>"Great!", "Super Combo!", "Unbelievable!"</em></p>
                </div>
                <div class="step-item">
                    <span class="step-number">BƯỚC 05</span>
                    <h4>Quy Tắc Vàng: Giữ Trống Vùng 3×3</h4>
                    <p><strong>Chiến thuật cao thủ:</strong> Luôn duy trì một khoảng trống 3×3 ở khu vực trung tâm bàn cờ. Điều này giúp bạn không bao giờ bị xử thua bất ngờ khi xuất hiện khối vuông 3×3 khổng lồ!</p>
                </div>
                <div class="step-item">
                    <span class="step-number">BƯỚC 06</span>
                    <h4>Chơi Offline 100% & Trợ Năng ADA</h4>
                    <p>Hoàn toàn không cần kết nối mạng Wi-Fi hay 4G. Tích hợp chế độ mù màu ADA với ký hiệu hình học trực quan, bảo vệ mắt và thân thiện với trẻ nhỏ.</p>
                </div>
            </div>
            <div style="margin-top: 36px; padding-top: 24px; border-top: 1px solid rgba(255,255,255,0.15); display: flex; gap: 16px; align-items: center; flex-wrap: wrap;">
                <a class="button" href="/vi/block-puzzle/privacy/" style="background:#00e5ff; color:#000; font-weight:800;">Chính Sách Bảo Mật →</a>
                <a class="button" href="/vi/block-puzzle/terms/" style="background:#1e293b; color:#fff; font-weight:700;">Điều Khoản Sử Dụng →</a>
                <a class="text-link" href="mailto:game@dvk.vn" style="color:#00e5ff;">Cần trợ giúp? Liên hệ game@dvk.vn →</a>
            </div>
        </section>'''

        spark = f'''<section id="catalog" style="padding: 20px 48px 50px;">
            <div class="project-heading">
                <div>
                    <p class="eyebrow" style="color:var(--muted);">DỰ ÁN KHÁC TỪ DVK</p>
                    <h2 style="color:#fff; margin: 4px 0 0;">Bộ Sưu Tập Trò Chơi Indie</h2>
                </div>
            </div>
            <article class="project-card" data-game="puzzle-spark" style="margin-top: 24px;">
                <div class="project-copy">
                    <div class="project-identity">
                        <img src="/assets/puzzle-spark-icon.png" width="72" height="72" alt="Puzzle Spark Icon">
                        <div>
                            <span class="project-index">02 / GAME LOGIC</span>
                            <h3>Puzzle Spark</h3>
                        </div>
                    </div>
                    <p>Game giải đố Lights Out thư thái và tĩnh lặng. Tắt hết các ô sáng qua 240 màn thử thách được tính toán kỹ lưỡng, không giới hạn thời gian. Hỗ trợ 5 ngôn ngữ.</p>
                    <div class="project-facts">
                        <span>240 màn giải đố</span>
                        <span>24 tầng độ khó</span>
                        <span>5 ngôn ngữ</span>
                    </div>
                    <div style="display:flex;gap:14px;align-items:center;flex-wrap:wrap;">
                        <a class="button" href="{url(PATHS['game'], lang)}" style="background:#173e30; color:#fff;">Khám phá Puzzle Spark ↗</a>
                        <a class="text-link" href="{url(PATHS['privacy'], lang)}" style="color:#616f65;">Quyền riêng tư →</a>
                    </div>
                </div>
                {grid(TEXT['vi'])}
            </article>
        </section>'''

        return hero + gallery + modes + boosters + mechanics + spark

def catalog(lang):
    vi = lang == 'vi'
    allhome = home(lang)
    projects = allhome[allhome.index('<section id="modes"'):allhome.index('<section id="catalog"')]
    title = 'Game Di Động Từ DVK' if vi else 'Mobile Games by DVK'
    intro = 'Khám phá các tựa game rèn luyện trí tuệ và giải trí sảng khoái từ DVK.' if vi else 'Explore thoughtful, beautifully crafted mobile puzzle games by DVK.'
    return '<section class="page-head catalog-head"><p class="eyebrow">DVK / ' + ('TRÒ CHƠI' if vi else 'GAMES') + '</p><h1>' + title + '</h1><p class="lead">' + intro + '</p></section>' + projects + '<div class="catalog-end"></div>'

def block_game(lang):
    # The dedicated block puzzle page uses the comprehensive home content
    return home(lang)

def game(lang):
    t = TEXT[lang]
    sections = [(t['gamelead'], t['details']), (t['hints'], t['hintbody']), (t['five'], t['fivebody'])]
    rows = ''.join('<section class="detail-row"><h2>' + esc(a) + '</h2><p>' + esc(b) + '</p></section>' for a, b in sections)
    helptext = ''.join('<details><summary>' + esc(a) + '</summary>' + paragraph(b) + '</details>' for a, b in DATA['help'][lang])
    return f'''<section class="page-head game-page-head"><div><p class="eyebrow">PUZZLE SPARK</p><h1>{'Puzzle Spark — Giải đố Lights Out' if lang == 'vi' else 'Puzzle Spark — Lights Out puzzles'}</h1><p class="lead">{esc(t['game_intro'])}</p><span class="pill">{esc(t['status'])}</span><p class="quiet">{'Đang chuẩn bị phát hành Android. Chưa công bố lịch phát hành iOS.' if lang == 'vi' else 'Android release in preparation. No public iOS release date has been announced.'}</p></div>{grid(t)}</section><div class="detail-wrap">{rows}<section class="help"><h2>{esc(t['how'])}</h2>{helptext}</section><p class="quiet">{esc(t['notmoney'])}</p><a class="button" href="{url(PATHS['support'], lang)}">{esc(t['contact'])} ↗</a></div>'''

def block_legal(kind, lang):
    t = TEXT[lang]
    data_key = 'block_privacy' if 'privacy' in kind else 'block_terms'
    title_key = 'block_privacytitle' if 'privacy' in kind else 'block_termstitle'
    lead_key = 'block_privacylead' if 'privacy' in kind else 'block_termslead'

    sections = ''.join('<section id="section-' + str(i + 1) + '"><h2>' + esc(a) + '</h2>' + paragraph(b) + '</section>' for i, (a, b) in enumerate(DATA[data_key][lang]))
    web = '<section><h2>' + esc(t['webtitle']) + '</h2>' + paragraph(t['webbody']) + '<p><a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement">GitHub Privacy</a> · <a href="https://www.cloudflare.com/privacypolicy/">Cloudflare Privacy</a></p></section>' if 'privacy' in kind else ''
    return f'''<section class="page-head legal-head"><p class="eyebrow">BLOCK PUZZLE 8×8 · {esc(t['legalnote'])}</p><h1>{esc(t[title_key])}</h1><p class="lead">{esc(t[lead_key])}</p><p class="provider">{esc(t['provider'])}</p></section><div class="legal-body">{sections}{web}<a class="text-link" href="{url(PATHS['support'], lang)}">{esc(t['contact'])} →</a></div>'''

def legal(kind, lang):
    t = TEXT[lang]
    sections = ''.join('<section id="section-' + str(i + 1) + '"><h2>' + esc(a) + '</h2>' + paragraph(b) + '</section>' for i, (a, b) in enumerate(DATA[kind][lang]))
    web = '<section><h2>' + esc(t['webtitle']) + '</h2>' + paragraph(t['webbody']) + '<p><a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement">GitHub Privacy</a> · <a href="https://www.cloudflare.com/privacypolicy/">Cloudflare Privacy</a></p></section>' if kind == 'privacy' else ''
    return f'''<section class="page-head legal-head"><p class="eyebrow">PUZZLE SPARK · {esc(t['legalnote'])}</p><h1>{esc(t[kind + 'title'])}</h1><p class="lead">{esc(t[kind + 'lead'])}</p><p class="provider">{esc(t['provider'])}</p></section><div class="legal-body">{sections}{web}<a class="text-link" href="{url(PATHS['support'], lang)}">{esc(t['contact'])} →</a></div>'''

def siteprivacy(lang):
    t = TEXT[lang]
    vi = lang == 'vi'
    title = 'Quyền riêng tư trên dvk.vn' if vi else 'Privacy on dvk.vn'
    intro = 'Chính sách dành cho website giới thiệu DVK. Mỗi ứng dụng có chính sách dữ liệu riêng.' if vi else 'Privacy information for the DVK website. Each app has its own data policy.'
    return '<section class="page-head legal-head"><p class="eyebrow">DVK / 18 OCT 2026</p><h1>' + title + '</h1><p class="lead">' + intro + '</p></section><div class="legal-body"><section><h2>' + esc(t['webtitle']) + '</h2>' + paragraph(t['webbody']) + '<p><a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement">GitHub Privacy</a> · <a href="https://www.cloudflare.com/privacypolicy/">Cloudflare Privacy</a></p></section><section><h2>' + ('Quyền riêng tư từng ứng dụng' if vi else 'App-specific privacy') + '</h2><p><a href="' + url(PATHS['block_privacy'], lang) + '"><strong>Block Puzzle 8×8: Neon Master</strong> — ' + esc(t['privacy']) + '</a></p><p><a href="' + url(PATHS['privacy'], lang) + '">Puzzle Spark — ' + esc(t['privacy']) + '</a></p></section><section><h2>' + esc(t['contact']) + '</h2><p><a href="mailto:game@dvk.vn">game@dvk.vn</a></p></section></div>'

def support(lang):
    t = TEXT[lang]
    rows = ''.join('<section><h2>' + esc(t[a]) + '</h2><p>' + esc(t[b]) + '</p></section>' for a, b in [('reporttitle', 'report'), ('savedtitle', 'saved'), ('notifytitle', 'notify')])
    return f'''<section class="page-head"><p class="eyebrow">DVKAPP / SUPPORT</p><h1>{esc(t['supporttitle'])}</h1><p class="lead">{esc(t['supportlead'])}</p></section><div class="support-layout"><aside class="contact-card"><img src="/assets/dvk-mark.svg" width="56" height="56" alt=""><h2>{esc(t['email'])}</h2><a class="email" href="mailto:game@dvk.vn?subject=Game%20Support">game@dvk.vn ↗</a><p>{esc(t['provider'])}</p></aside><div class="support-copy">{rows}</div></div>'''

# Build all pages in English (default) and Vietnamese
for lang in ['en', 'vi']:
    for kind, path in PATHS.items():
        if kind == 'home':
            body = home(lang)
            title = 'Block Puzzle 8×8: Neon Master — Game Xếp Hình 8x8 & Cốt Truyện' if lang == 'vi' else 'Block Puzzle 8x8: Neon Master — Official Game & Studio Showcase'
        elif kind == 'catalog':
            body = catalog(lang)
            title = 'Trò chơi' if lang == 'vi' else 'Games'
        elif kind == 'block_game':
            body = block_game(lang)
            title = 'Block Puzzle 8×8: Neon Master'
        elif kind == 'block_privacy' or kind == 'block_terms':
            body = block_legal(kind, lang)
            title = TEXT[lang][('block_privacytitle' if kind == 'block_privacy' else 'block_termstitle')]
        elif kind == 'game':
            body = game(lang)
            title = 'Puzzle Spark'
        elif kind == 'privacy' or kind == 'terms':
            body = legal(kind, lang)
            title = TEXT[lang][kind + 'title']
        elif kind == 'siteprivacy':
            body = siteprivacy(lang)
            title = 'Quyền riêng tư website' if lang == 'vi' else 'Website privacy'
        elif kind == 'support':
            body = support(lang)
            title = TEXT[lang]['supporttitle']

        dest = OUT / url(path, lang).lstrip('/')
        dest.mkdir(parents=True, exist_ok=True)
        (dest / 'index.html').write_text(shell(kind, lang, body, title), encoding='utf-8')

# Keep legacy URL redirects
for lang in ['en', 'vi']:
    for old, new in [('/game1/', PATHS['game']), ('/game1/privacy/', PATHS['privacy']), ('/game1/terms/', PATHS['terms']), ('/game2/', PATHS['block_game']), ('/game2/privacy/', PATHS['block_privacy']), ('/game2/terms/', PATHS['block_terms'])]:
        target = url(new, lang)
        dest = OUT / url(old, lang).lstrip('/')
        dest.mkdir(parents=True, exist_ok=True)
        (dest / 'index.html').write_text(
            '<!doctype html><html lang="' + lang + '"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><link rel="canonical" href="' + BASE + target + '"><meta http-equiv="refresh" content="0;url=' + target + '"><title>DVK</title></head><body><p><a href="' + target + '">Continue →</a></p></body></html>',
            encoding='utf-8',
        )

(OUT / 'app-ads.txt').write_text('google.com, pub-3636940103463538, DIRECT, f08c47fec0942fa0\n', encoding='utf-8')
(OUT / 'CNAME').write_text('dvk.vn\n', encoding='utf-8')
(OUT / '.nojekyll').touch()
(OUT / 'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: https://dvk.vn/sitemap.xml\n', encoding='utf-8')

locs = [BASE + url(p, l) for l in ['en', 'vi'] for p in PATHS.values()]
(OUT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join('<url><loc>' + x + '</loc></url>' for x in locs) + '</urlset>', encoding='utf-8')
(OUT / '404.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found · DVK</title><meta name="robots" content="noindex"><link rel="stylesheet" href="/assets/site.css"><main class="page-head"><p class="eyebrow">404</p><h1>A different path.</h1><p>This page could not be found.</p><a class="button" href="/">Back to DVKapp</a></main></html>', encoding='utf-8')

print('Built', len(locs), 'pages and app-ads.txt in', OUT)

# Copy to docs/ for GitHub Pages publishing
pages = ROOT / 'docs'
if pages.exists():
    shutil.rmtree(pages)
shutil.copytree(OUT, pages)
print('Successfully synced dist/ to docs/ for GitHub Pages!')
