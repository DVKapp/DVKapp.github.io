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

TEXT = {
    'en': {
        'nav': ['Games', 'Privacy', 'Support'],
        'lang': 'Tiếng Việt',
        'tag': 'INDEPENDENT APPS & GAMES',
        'title': 'A little quiet.\nA brighter idea.',
        'intro': 'Thoughtful games built for focus and fun. Discover Block Puzzle 8x8: Neon Master and Puzzle Spark.',
        'explore': 'Discover Puzzle Spark',
        'explore_block': 'Explore Block Puzzle 8x8',
        'contact': 'Get in touch',
        'status': 'Preview build · Store release in preparation',
        'block_status': 'v1.0.0 Ready · App Store & Google Play',
        'foot': 'Small games. Space to think.',
        'terms': 'Terms',
        'privacy': 'Privacy',
        'support': 'Support',
        'game_intro': 'Turn every light off. Each tap changes a cell and its edge-sharing neighbors. A simple rule, with room to think.',
        'block_intro': 'Master the 8×8 neon grid! Blast lines, trigger blazing combo multipliers, conquer 20 Story Saga stages, compete in Live Events, and play 100% offline.',
        'block_lead': '8 Exciting Modes. Infinite Joy.',
        'block_details': 'Classic Endless, Story Saga with 20 stages unlocking Galaxy themes, Online Live Tournaments, Monthly 31-day Cup, Daily Quests with 21-day streaks, Global Leaderboards, Themes Shop, and ADA Accessibility.',
        'block_boosters': 'Tactical Boosters & Smart Foresight',
        'block_boosters_body': 'Undo tricky drops, Rotate tray shapes, Hammer blast 3×3 obstacles, and preview upcoming blocks in advance.',
        'block_offline': 'Pure Offline & ADA Accessible',
        'block_offline_body': 'No Wi-Fi or data required. Full colorblind high-contrast modes, dynamic voice cheering, and kid-friendly candy-neon design.',
        'block_privacytitle': 'Block Puzzle 8x8 Privacy Policy',
        'block_privacylead': 'Clear, transparent privacy principles for Block Puzzle 8x8: Neon Master. No accounts, no personal tracking, and local progress storage.',
        'block_termstitle': 'Block Puzzle 8x8 Terms of Use',
        'block_termslead': 'Terms of use, virtual coins, IAP policies, and player guidelines for Block Puzzle 8x8: Neon Master.',
        'how': 'Game Rules & Mechanics',
        'legalnote': 'Official Policy · Updated 18 October 2026',
        'provider': 'Developer brand: DVKapp. Support: game@dvk.vn.',
        'webtitle': 'About this website',
        'webbody': 'This website has no account, contact form, advertising SDK, analytics script or tracking cookie. Email opens your own mail app. Hosted on GitHub Pages and managed through Cloudflare.',
        'notmoney': 'Coins, stars and trophies are in-game records and cannot be exchanged for cash.',
        'supporttitle': 'A little help, when you need it.',
        'supportlead': 'Questions, bug report, or ideas for our games? Contact DVKapp directly.',
        'email': 'Email support',
        'reporttitle': 'Help us reproduce a problem',
        'report': 'Include your app version, device model, operating system, level number and the steps that led to the issue. Never send passwords or payment details.',
        'savedtitle': 'About saved progress',
        'saved': 'Progress is stored on your device. Please do not uninstall or reset data while troubleshooting if you want to keep your records.',
        'notifytitle': 'Reminders are optional',
        'notify': 'Local reminders can be enabled or disabled in the app Settings.',
        'gamelead': 'One rule. A whole journey.',
        'details': '240 unique puzzles, arranged into 24 tiers of 10. Start with 3×3, progress to 4×4 and 5×5.',
        'hints': 'Help, on your terms.',
        'hintbody': 'Two free daily hints and voluntary rewarded ads in development builds.',
        'five': 'Five languages. One spark.',
        'fivebody': 'English, Vietnamese, Spanish, Portuguese and Japanese available in Settings.',
        'privacytitle': 'Your privacy, in plain words.',
        'privacylead': 'This policy describes the current Puzzle Spark preview and this website.',
        'termstitle': 'Terms of use',
        'termslead': 'The terms for the current Puzzle Spark preview.',
        'gridlabel': 'Illustration of a Lights Out puzzle',
    },
    'vi': {
        'nav': ['Trò chơi', 'Quyền riêng tư', 'Hỗ trợ'],
        'lang': 'English',
        'tag': 'ỨNG DỤNG & TRÒ CHƠI ĐỘC LẬP',
        'title': 'Một chút tĩnh lặng.\nMột ý tưởng sáng lên.',
        'intro': 'Những trò chơi rèn luyện trí tuệ và giải trí sảng khoái. Khám phá Block Puzzle 8x8: Neon Master và Puzzle Spark.',
        'explore': 'Khám phá Puzzle Spark',
        'explore_block': 'Khám phá Block Puzzle 8x8',
        'contact': 'Liên hệ',
        'status': 'Bản thử nghiệm · Đang chuẩn bị phát hành',
        'block_status': 'Sẵn sàng v1.0.0 · App Store & Google Play',
        'foot': 'Trò chơi nhỏ. Khoảng trời suy nghĩ.',
        'terms': 'Điều khoản',
        'privacy': 'Quyền riêng tư',
        'support': 'Hỗ trợ',
        'game_intro': 'Tắt hết các ô sáng. Mỗi lần chạm sẽ đổi trạng thái một ô và các ô chung cạnh.',
        'block_intro': 'Chinh phục lưới 8×8 rực rỡ neon! Phá hủy hàng cột, kích hoạt chuỗi Combo bão điểm, vượt 20 ải Cốt truyện, đua cúp trực tuyến và chơi offline 100% không cần mạng.',
        'block_lead': '8 Chế Độ Chơi Đỉnh Cao. Niềm Vui Bất Tận.',
        'block_details': 'Chơi Cổ Điển Vô Tận, Cốt Truyện Saga 20 ải mở khóa chủ đề Galaxy, Giải Đấu Đua Cúp Trực Tuyến, Thử Thách Tháng 31 ngày, Điểm Danh 21 ngày, Bảng Xếp Hạng Toàn Cầu, Cửa Hàng Giao Diện và Chế Độ Trợ Năng Mù Màu ADA.',
        'block_boosters': 'Bộ 3 Bảo Bối Cứu Nguy & Xem Trước Khối',
        'block_boosters_body': 'Hoàn Tác (Undo) nước đi hiểm, Đổi Chiều (Rotate) khối xếp, Búa Phá Hủy (Hammer 3×3) giải phóng không gian và Mở Ẩn Xem Trước 3 Khối Kế Tiếp.',
        'block_offline': 'Chơi Hoàn Toàn Offline & Thân Thiện Trẻ Em',
        'block_offline_body': '100% không cần kết nối Wi-Fi hay 4G/5G. Giao diện kẹo ngọt Candy-Neon sắc nét, chữ to rõ ràng, âm thanh cổ vũ tiếng Anh sống động và hỗ trợ mù màu ADA.',
        'block_privacytitle': 'Chính Sách Quyền Riêng Tư Block Puzzle 8x8',
        'block_privacylead': 'Quy định bảo mật minh bạch cho Block Puzzle 8x8: Neon Master. Không yêu cầu tài khoản, không theo dõi cá nhân, bảo mật giao dịch IAP tuyệt đối.',
        'block_termstitle': 'Điều Khoản Sử Dụng Block Puzzle 8x8',
        'block_termslead': 'Điều khoản sử dụng, quy định xu ảo, vật phẩm bảo bối và gói gỡ quảng cáo vĩnh viễn trong Block Puzzle 8x8: Neon Master.',
        'how': 'Luật Chơi & Kỹ Năng Đỉnh Cao',
        'legalnote': 'Chính sách chính thức · Cập nhật 18/10/2026',
        'provider': 'Thương hiệu phát triển: DVKapp. Hỗ trợ: game@dvk.vn.',
        'webtitle': 'Về website này',
        'webbody': 'Website không có tài khoản, biểu mẫu liên hệ, SDK quảng cáo hay cookie theo dõi. Lưu trữ trên GitHub Pages và quản lý qua Cloudflare.',
        'notmoney': 'Xu vàng, bảo bối và cúp sao là thành tích trong trò chơi, không phải tiền hoặc hiện vật.',
        'supporttitle': 'Một chút trợ giúp, khi bạn cần.',
        'supportlead': 'Bạn có câu hỏi, gặp lỗi hoặc có ý tưởng đóng góp cho game? Hãy liên hệ trực tiếp với DVKapp.',
        'email': 'Hỗ trợ qua email',
        'reporttitle': 'Giúp chúng tôi tái hiện lỗi',
        'report': 'Gửi phiên bản app, dòng máy, hệ điều hành và các bước dẫn tới lỗi. Không gửi mật khẩu hay thông tin thanh toán.',
        'savedtitle': 'Về tiến độ đã lưu',
        'saved': 'Tiến độ được lưu an toàn trên thiết bị của bạn.',
        'notifytitle': 'Nhắc hẹn là tùy chọn',
        'notify': 'Bạn có thể bật hoặc tắt thông báo trong phần Cài đặt của game.',
        'gamelead': 'Một quy luật. Cả một hành trình.',
        'details': '240 bảng khác nhau, chia 24 tầng, mỗi tầng 10 màn. Bắt đầu với lưới 3×3, tiến tới 4×4 và 5×5.',
        'hints': 'Trợ giúp theo lựa chọn của bạn.',
        'hintbody': 'Mỗi ngày có hai gợi ý miễn phí và quảng cáo nhận thưởng tự nguyện trong bản phát triển.',
        'five': 'Năm ngôn ngữ. Chung một tia sáng.',
        'fivebody': 'Mặc định tiếng Anh; có thể chọn tiếng Việt, Tây Ban Nha, Bồ Đào Nha hoặc Nhật.',
        'privacytitle': 'Quyền riêng tư, trình bày rõ ràng.',
        'privacylead': 'Chính sách mô tả bản thử nghiệm Puzzle Spark hiện tại và website này.',
        'termstitle': 'Điều khoản sử dụng',
        'termslead': 'Điều khoản dành cho bản thử nghiệm Puzzle Spark hiện tại.',
        'gridlabel': 'Hình minh họa bảng giải đố Lights Out',
    }
}

SEO = {
    'en': {
        'home': ('DVK — Mobile Apps & Block Puzzle Games', 'Discover mobile games by DVK, including Block Puzzle 8x8: Neon Master and Puzzle Spark. Features, rules, instructions, privacy policies, and developer support.'),
        'catalog': ('Games by DVK — Block Puzzle 8x8 & Puzzle Spark', 'Explore indie mobile games by DVK. Meet Block Puzzle 8x8: Neon Master with 8 modes and Story Saga, and Puzzle Spark with 240 logic puzzles.'),
        'siteprivacy': ('DVK Website Privacy Policy', 'Learn about privacy on dvk.vn, website hosting and game data handling policies.'),
        'support': ('DVK Support — Game Help & Bug Reports', 'Get direct support for Block Puzzle 8x8: Neon Master and Puzzle Spark. Contact game@dvk.vn.'),
        'game': ('Puzzle Spark — Lights Out Logic Puzzle | DVK', 'Explore Puzzle Spark: 240 Lights Out puzzles across 24 difficulty tiers, daily challenges, hints and five languages.'),
        'privacy': ('Puzzle Spark Privacy Policy | DVK', 'Read how the Puzzle Spark preview handles local progress, reminders, and advertising.'),
        'terms': ('Puzzle Spark Terms of Use | DVK', 'Terms of use for the Puzzle Spark preview: game progress, hints, and support.'),
        'block_game': ('Block Puzzle 8x8: Neon Master — Classic Grid & Story Saga | DVK', 'Master the 8x8 neon grid! 8 candy-neon modes, 20 Story Saga stages, online live events, tactical boosters, combo streaks, and pure offline play on iOS and Android.'),
        'block_privacy': ('Block Puzzle 8x8 Privacy Policy | DVK', 'Official privacy policy for Block Puzzle 8x8: Neon Master. Details on on-device data storage, in-app purchases, and Google AdMob integration.'),
        'block_terms': ('Block Puzzle 8x8 Terms of Use | DVK', 'Official terms of use for Block Puzzle 8x8: Neon Master. Rules on virtual coins, boosters, permanent No-Ads package, and fair play.'),
    },
    'vi': {
        'home': ('DVK — Ứng dụng & Game Giải Đố Di Động', 'Khám phá các tựa game từ DVK: Block Puzzle 8x8: Neon Master và Puzzle Spark. Tìm hiểu tính năng, hướng dẫn chơi, chính sách bảo mật và hỗ trợ.'),
        'catalog': ('Trò Chơi Từ DVK — Block Puzzle 8x8 & Puzzle Spark', 'Bộ sưu tập game di động độc lập từ DVK: Trải nghiệm xếp hình Block Puzzle 8x8 phong cách neon và giải đố trí tuệ Puzzle Spark.'),
        'siteprivacy': ('Quyền riêng tư website DVK', 'Tìm hiểu quyền riêng tư trên dvk.vn, dịch vụ lưu trữ website và chính sách bảo mật ứng dụng.'),
        'support': ('Hỗ trợ DVK — Trợ giúp Game & Báo Lỗi', 'Nhận trợ giúp trực tiếp cho Block Puzzle 8x8: Neon Master và Puzzle Spark. Liên hệ email game@dvk.vn.'),
        'game': ('Puzzle Spark — Game giải đố Lights Out | DVK', 'Khám phá 240 màn Lights Out qua 24 tầng khó, thử thách hằng ngày và gợi ý trong Puzzle Spark.'),
        'privacy': ('Quyền riêng tư Puzzle Spark | DVK', 'Thông tin dữ liệu của bản thử nghiệm Puzzle Spark: tiến độ trên thiết bị, nhắc nhở và quảng cáo.'),
        'terms': ('Điều khoản Puzzle Spark | DVK', 'Điều khoản sử dụng bản thử nghiệm Puzzle Spark, gồm tiến độ, gợi ý và hỗ trợ.'),
        'block_game': ('Block Puzzle 8x8: Neon Master — Game Xếp Hình 8x8 & Cốt Truyện | DVK', 'Game xếp hình 8x8 đỉnh cao phong cách neon rực rỡ! 8 chế độ game, 20 ải Cốt truyện, giải đấu trực tuyến, bảo bối cứu nguy, chơi offline 100% không cần mạng.'),
        'block_privacy': ('Chính sách Quyền riêng tư Block Puzzle 8x8 | DVK', 'Chính sách bảo mật chính thức cho Block Puzzle 8x8: Neon Master: Lưu trữ tiến độ cục bộ, thanh toán IAP an toàn, quảng cáo thân thiện.'),
        'block_terms': ('Điều khoản Sử dụng Block Puzzle 8x8 | DVK', 'Điều khoản sử dụng Block Puzzle 8x8: Neon Master: Quy định xu vàng, bảo bối cứu nguy, gói gỡ quảng cáo vĩnh viễn và hỗ trợ người chơi.'),
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

    if kind == 'block_game':
        game = {
            '@type': 'VideoGame',
            '@id': BASE + '/block-puzzle/#game',
            'name': 'Block Puzzle 8x8: Neon Master',
            'url': canonical,
            'description': desc,
            'genre': 'Block Puzzle, Logic, Brain Training',
            'gamePlatform': ['iOS', 'Android'],
            'inLanguage': ['en', 'vi'],
            'image': BASE + '/assets/block-puzzle-icon.png',
            'publisher': {'@id': BASE + '/#organization'},
            'applicationCategory': 'Game',
            'operatingSystem': 'iOS, Android',
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

def block_art():
    return '<div class="block-art"><img src="/assets/block-puzzle-preview.png" alt="Block Puzzle 8x8 Neon Master Gameplay Screenshot" width="390" height="844" loading="lazy"></div>'

def shell(kind, lang, body, title):
    t = TEXT[lang]
    path = PATHS[kind]
    theme = 'block-puzzle' if 'block' in kind else 'puzzle-spark' if kind in ['game', 'privacy', 'terms'] else 'dvk'
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
    if theme == 'block-puzzle':
        crumbs = '<nav class="breadcrumbs" aria-label="Breadcrumb"><a href="' + url('/', lang) + '">DVK</a><span>/</span><a href="' + url(PATHS['catalog'], lang) + '">' + ('Trò chơi' if lang == 'vi' else 'Games') + '</a><span>/</span>'
        crumbs += ('<span aria-current="page">Block Puzzle 8x8</span>' if kind == 'block_game' else '<a href="' + url(PATHS['block_game'], lang) + '">Block Puzzle 8x8</a><span>/</span><span aria-current="page">' + esc(t['privacy'] if 'privacy' in kind else t['terms']) + '</span>') + '</nav>'
    elif theme == 'puzzle-spark':
        crumbs = '<nav class="breadcrumbs" aria-label="Breadcrumb"><a href="' + url('/', lang) + '">DVK</a><span>/</span><a href="' + url(PATHS['catalog'], lang) + '">' + ('Trò chơi' if lang == 'vi' else 'Games') + '</a><span>/</span>'
        crumbs += ('<span aria-current="page">Puzzle Spark</span>' if kind == 'game' else '<a href="' + url(PATHS['game'], lang) + '">Puzzle Spark</a><span>/</span><span aria-current="page">' + esc(t[kind]) + '</span>') + '</nav>'

    logo = '/assets/block-puzzle-icon.png' if theme == 'block-puzzle' else '/assets/spark.svg' if theme == 'puzzle-spark' else '/assets/dvk-mark.svg'
    ogimage = '/assets/block-puzzle-preview.png' if theme == 'block-puzzle' else '/assets/puzzle-spark-icon.png' if theme == 'puzzle-spark' else '/assets/dvk-mark.svg'

    theme_color = '#090d1a' if theme == 'block-puzzle' else '#173e30' if theme == 'puzzle-spark' else '#152642'

    return f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="google-site-verification" content="VCgA69MCS2iiEJBLr5-Sl772K8mIju2FWOCB73ZwFCE"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><meta name="theme-color" content="{theme_color}"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{canonical}"><link rel="alternate" hreflang="en" href="{BASE + path}"><link rel="alternate" hreflang="vi" href="{BASE + url(path, 'vi')}"><link rel="alternate" hreflang="x-default" href="{BASE + path}"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{canonical}"><meta property="og:type" content="website"><meta property="og:site_name" content="DVK"><meta property="og:locale" content="{'vi_VN' if lang == 'vi' else 'en_US'}"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(desc)}"><meta property="og:image" content="{BASE}{ogimage}"><link rel="icon" type="image/png" href="{logo}"><link rel="stylesheet" href="/assets/site.css">{schema}</head><body data-theme="{theme}"><a class="skip" href="#main">{'Skip to content' if lang == 'en' else 'Đến nội dung'}</a><header><a class="brand" href="{url('/', lang)}" aria-label="DVK home"><img src="/assets/dvk-mark.svg" alt="" width="34" height="34">DVK</a><nav aria-label="{'Main navigation' if lang == 'en' else 'Điều hướng chính'}">{nav}<a class="language" href="{url(path, other)}" lang="{other}" hreflang="{other}">{esc(t['lang'])}</a></nav></header><main id="main">{crumbs}{body}</main><footer><div><a class="brand" href="{url('/', lang)}">DVK</a><p>{esc(t['foot'])}</p><a href="mailto:game@dvk.vn">game@dvk.vn</a></div><div class="footer-links">{footer}</div><small>© 2026 DVK · Apps & Games</small></footer></body></html>'''

def home(lang):
    t = TEXT[lang]
    vi = lang == 'vi'
    title = 'Ý tưởng nhỏ.<br>Trải nghiệm đáng nhớ.' if vi else 'Small ideas.<br>Memorable experiences.'
    intro = 'DVK phát triển ứng dụng và trò chơi cho thiết bị di động. Khám phá các dự án, tìm hiểu từng game và nhận hỗ trợ trực tiếp tại đây.' if vi else 'DVK builds mobile apps and games. Explore our projects, get to know each game, and find direct support in one place.'
    hero = '<section class="hero studio-hero"><div class="hero-copy"><p class="eyebrow">DVK / ' + ('ỨNG DỤNG & TRÒ CHƠI' if vi else 'APPS & GAMES') + '</p><h1>' + title + '</h1><p class="lead">' + intro + '</p><div class="actions"><a class="button" href="#games">' + ('Khám phá dự án' if vi else 'Explore our projects') + ' <span aria-hidden="true">↘</span></a><a class="text-link" href="' + url(PATHS['support'], lang) + '">' + t['contact'] + ' →</a></div></div><div class="studio-art" aria-hidden="true"><div class="studio-card studio-back"></div><div class="studio-card studio-front"><img src="/assets/dvk-mark.svg" alt="" width="65" height="65"><strong>DVK<span>✦</span></strong><small>IDEAS INTO EXPERIENCES</small></div></div></section>'
    heading = 'Ứng dụng & trò chơi' if vi else 'Apps & games'

    # Project 1: Block Puzzle 8x8 (Flagship)
    block_card = f'''<article class="project-card" data-game="block-puzzle" style="margin-bottom: 36px;">
        <div class="project-copy">
            <div class="project-identity">
                <img src="/assets/block-puzzle-icon.png" width="72" height="72" alt="Block Puzzle 8x8 Neon Master Icon" style="border-radius:18px;">
                <div>
                    <span class="project-index">01 / FLAGSHIP · BLOCK PUZZLE</span>
                    <h3>Block Puzzle 8×8: Neon Master</h3>
                </div>
            </div>
            <p>{esc(t['block_intro'])}</p>
            <div class="project-facts">
                <span>8 {'chế độ chơi' if vi else 'game modes'}</span>
                <span>20 {'ải cốt truyện' if vi else 'story stages'}</span>
                <span>{'Chơi offline 100%' if vi else 'Pure offline play'}</span>
                <span>{'Trợ năng mù màu ADA' if vi else 'ADA accessible'}</span>
            </div>
            <div style="display:flex;gap:14px;align-items:center;flex-wrap:wrap;">
                <a class="button" href="{url(PATHS['block_game'], lang)}">{esc(t['explore_block'])} ↗</a>
                <a class="text-link" href="{url(PATHS['block_privacy'], lang)}" style="color:var(--muted);">{esc(t['privacy'])} →</a>
            </div>
            <p class="project-status" style="margin-top:14px;color:#00e5ff;">✦ {esc(t['block_status'])}</p>
        </div>
        {block_art()}
    </article>'''

    # Project 2: Puzzle Spark
    spark_card = f'''<article class="project-card" data-game="puzzle-spark">
        <div class="project-copy">
            <div class="project-identity">
                <img src="/assets/puzzle-spark-icon.png" width="72" height="72" alt="Puzzle Spark">
                <div>
                    <span class="project-index">02 / LOGIC PUZZLE</span>
                    <h3>Puzzle Spark</h3>
                </div>
            </div>
            <p>{esc(t['game_intro'])}</p>
            <div class="project-facts">
                <span>240 {'màn' if vi else 'puzzles'}</span>
                <span>24 {'tầng' if vi else 'tiers'}</span>
                <span>5 {'ngôn ngữ' if vi else 'languages'}</span>
            </div>
            <div style="display:flex;gap:14px;align-items:center;flex-wrap:wrap;">
                <a class="button" href="{url(PATHS['game'], lang)}">{esc(t['explore'])} ↗</a>
                <a class="text-link" href="{url(PATHS['privacy'], lang)}" style="color:var(--muted);">{esc(t['privacy'])} →</a>
            </div>
            <p class="project-status" style="margin-top:14px;">✦ {esc(t['status'])}</p>
        </div>
        {grid(t)}
    </article>'''

    project = f'<section id="games" class="projects"><div class="project-heading"><p class="eyebrow">' + ('KHÁM PHÁ CÙNG DVK' if vi else 'DISCOVER DVK') + f'</p><h2>{heading}</h2></div>{block_card}{spark_card}</section>'

    items = [
        ('Dành cho thiết bị di động', 'Trải nghiệm mượt mà được xây dựng cho iOS và Android với tốc độ 60fps/120fps.'),
        ('Thông tin rõ ràng & Minh bạch', 'Mỗi tựa game có hướng dẫn, chính sách quyền riêng tư và điều khoản sử dụng riêng biệt.'),
        ('Hỗ trợ trực tiếp từ lập trình viên', 'Mọi thắc mắc, phản hồi hoặc yêu cầu hỗ trợ được tiếp nhận trực tiếp qua email game@dvk.vn.'),
    ] if vi else [
        ('Built for mobile', 'Smooth 60fps/120fps experiences crafted natively for iOS and Android.'),
        ('Clear & transparent policies', 'Every game features its own dedicated guide, privacy policy, and terms.'),
        ('Direct developer support', 'Get in touch directly with our development team at game@dvk.vn.'),
    ]
    features = '<section class="features">' + ''.join('<article><span class="feature-number">0' + str(i + 1) + '</span><h3>' + esc(a) + '</h3><p>' + esc(b) + '</p></article>' for i, (a, b) in enumerate(items)) + '</section>'
    return hero + project + features

def catalog(lang):
    vi = lang == 'vi'
    allhome = home(lang)
    projects = allhome[allhome.index('<section id="games"'):allhome.index('<section class="features"')]
    title = 'Một nơi cho từng trải nghiệm.' if vi else 'A place for every experience.'
    intro = 'Khám phá trò chơi từ DVK. Mỗi game có phong cách riêng, cùng trang giới thiệu, hướng dẫn và hỗ trợ đầy đủ.' if vi else 'Discover games by DVK. Each game has its own identity, introduction, instructions and support.'
    return '<section class="page-head catalog-head"><p class="eyebrow">DVK / ' + ('TRÒ CHƠI' if vi else 'GAMES') + '</p><h1>' + title + '</h1><p class="lead">' + intro + '</p></section>' + projects + '<div class="catalog-end"></div>'

def block_game(lang):
    t = TEXT[lang]
    vi = lang == 'vi'
    sections = [
        (t['block_lead'], t['block_details']),
        (t['block_boosters'], t['block_boosters_body']),
        (t['block_offline'], t['block_offline_body']),
    ]
    rows = ''.join('<section class="detail-row"><h2>' + esc(a) + '</h2><p>' + esc(b) + '</p></section>' for a, b in sections)
    helptext = ''.join('<details><summary>' + esc(a) + '</summary>' + paragraph(b) + '</details>' for a, b in DATA['block_help'][lang])

    store_badges = f'''<div style="display:flex;gap:16px;align-items:center;flex-wrap:wrap;margin:24px 0 16px;">
        <span class="pill" style="font-weight:700;">iOS App Store (v1.0.0)</span>
        <span class="pill" style="font-weight:700;">Google Play Store</span>
        <span class="pill" style="font-weight:700;">Pure Offline</span>
        <span class="pill" style="font-weight:700;">No Wi-Fi Needed</span>
    </div>'''

    return f'''<section class="page-head game-page-head">
        <div>
            <p class="eyebrow">BLOCK PUZZLE 8×8 / NEON MASTER</p>
            <h1>{'Block Puzzle 8×8: Neon Master' if vi else 'Block Puzzle 8×8: Neon Master'}</h1>
            <p class="lead">{esc(t['block_intro'])}</p>
            {store_badges}
            <div style="display:flex;gap:14px;margin-top:16px;">
                <a class="button" href="{url(PATHS['block_privacy'], lang)}">{'Chính sách bảo mật' if vi else 'Privacy Policy'} →</a>
                <a class="button" href="{url(PATHS['block_terms'], lang)}" style="background:#1e293b;color:#fff;">{'Điều khoản' if vi else 'Terms of Use'} →</a>
            </div>
        </div>
        {block_art()}
    </section>
    <div class="detail-wrap">
        {rows}
        <section class="help">
            <h2>{esc(t['how'])}</h2>
            {helptext}
        </section>
        <p class="quiet">{esc(t['notmoney'])}</p>
        <a class="button" href="{url(PATHS['support'], lang)}">{esc(t['contact'])} ↗</a>
    </div>'''

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

# Build all pages in English and Vietnamese
for lang in ['en', 'vi']:
    for kind, path in PATHS.items():
        if kind == 'home':
            body = home(lang)
            title = 'DVK — Ứng dụng & game giải đố' if lang == 'vi' else 'DVK — Mobile Apps & Block Puzzle Games'
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
