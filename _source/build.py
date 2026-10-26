#!/usr/bin/env python3
"""Generates the Northland Plumbing, Gas & Drainage demo pages from one source of truth.
Run from anywhere: python3 _build/build.py  (needs the img/ folder already filled)."""
import html, json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "img"
SITE_URL = "https://northland-plumbing-gas-drainage-demo.vercel.app"
LOGO_INNER = (Path(__file__).parent / "logo-inner.txt").read_text()

NAME = "Northland Plumbing, Gas & Drainage"
GAS_TEL, GAS_TXT = "tel:08009268427", "0800 WANT GAS"
GAS_DIGITS = "0800 926 8427"
H2O_TEL, H2O_TXT, H2O_DIGITS = "tel:08009268426", "0800 WANT H2O", "0800 926 8426"
ADMIN_TEL, ADMIN_TXT = "tel:+6494300669", "09 430 0669"
EMAIL_USER, EMAIL_DOMAIN = "info", "northlandpg.co.nz"
ADDRESS = "140 Lower Dent Street, Whangārei 0110"
FB = "https://www.facebook.com/NorthlandPG/"
LRD = "0x6d0b7f5d0de557a1:0x5102cbeec86a214e"
G_REVIEWS = f"https://www.google.com/search?q=Northland+Plumbing+Gas+%26+Drainage+Whangarei#lrd={LRD},1,,,,"
G_WRITE = f"https://www.google.com/search?q=Northland+Plumbing+Gas+%26+Drainage+Whangarei#lrd={LRD},3,,,,"
MAPS = "https://www.google.com/maps/place/Northland+Plumbing+Gas+%26+Drainage/@-35.7273589,174.3290948,17z"
MAP_EMBED = "https://www.google.com/maps?q=Northland+Plumbing+Gas+%26+Drainage,+140+Lower+Dent+Street,+Whangarei&output=embed"
JOB_AD = "https://www.trademe.co.nz/a/jobs/trades-services/plumbing/northland/whangarei/full-time/listing/5898594577"

def e(s): return html.escape(s, quote=True)
def q(s): return s.replace("%", "%25").replace(" ", "%20").replace("\n", "%0A").replace(",", "%2C").replace("&", "%26").replace("?", "%3F").replace(":", "%3A").replace("'", "%27")

def gmail(subject, body):
    return ("https://mail.google.com/mail/?view=cm&amp;fs=1&amp;to=" + EMAIL_USER + "%40" + EMAIL_DOMAIN +
            "&amp;su=" + q(subject) + "&amp;body=" + q(body))
EMAIL_TEXT = EMAIL_USER + "&#64;" + EMAIL_DOMAIN

def dims(f):
    with Image.open(IMG / f) as im:
        return im.size

def pic(name, alt, sizes="100vw", cls="", eager=False, hero=False, extra="", prefix=""):
    """Responsive <img> for a photo that has -1080 and -1920 (and -3840 for hero) webp files."""
    w, h = dims(f"{name}-1920.webp")
    srcset = [f"{prefix}img/{name}-1080.webp 1080w", f"{prefix}img/{name}-1920.webp 1920w"]
    if hero:
        srcset.append(f"{prefix}img/{name}-3840.webp 3840w")
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="{prefix}img/{name}-1920.webp" srcset="{", ".join(srcset)}" sizes="{sizes}" '
            f'alt="{e(alt)}" width="{w}" height="{h}" {load}{extra}>')

# ---------------------------------------------------------------- icons
ICONS = """<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <symbol id="i-phone" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></symbol>
  <symbol id="i-mail" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16"/><path d="m22 7-10 6L2 7"/></symbol>
  <symbol id="i-pin" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/></symbol>
  <symbol id="i-clock" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></symbol>
  <symbol id="i-check" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="square"><path d="M20 6 9 17l-5-5"/></symbol>
  <symbol id="i-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="square"><path d="M5 12h14M13 5l7 7-7 7"/></symbol>
  <symbol id="i-flame" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22c4 0 7-2.7 7-6.8 0-3.6-2.4-5.9-4.1-8.3-.4 2-1.4 3.2-2.6 3.8C12.6 7.2 11 4.3 8.6 2c.2 3.4-3.6 6.6-3.6 11.2C5 18.6 8 22 12 22z"/><path d="M12 22c-1.7 0-3-1.3-3-3.1 0-1.9 1.6-3 3-4.9 1.4 1.9 3 3 3 4.9 0 1.8-1.3 3.1-3 3.1z"/></symbol>
  <symbol id="i-drop" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2.7 6.3 9.6a7.3 7.3 0 1 0 11.4 0z"/></symbol>
  <symbol id="i-shield" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></symbol>
  <symbol id="i-award" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="6"/><path d="M15.5 13.2 17 22l-5-3-5 3 1.5-8.8"/></symbol>
  <symbol id="i-truck" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 4h14v12H1zM15 9h4l4 4v3h-8z"/><circle cx="6" cy="18.5" r="2"/><circle cx="18" cy="18.5" r="2"/></symbol>
  <symbol id="i-wrench" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.8-3.8a6 6 0 0 1-7.9 7.9l-6.9 6.9a2.1 2.1 0 0 1-3-3l6.9-6.9a6 6 0 0 1 7.9-7.9z"/></symbol>
  <symbol id="i-hat" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 18h20M4 18v-3a8 8 0 0 1 16 0v3M10 7V5h4v2M12 7v6"/></symbol>
  <symbol id="i-digger" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="15" width="12" height="5" rx="2.5"/><path d="M4 15v-4h6l2 4M10 11V7l6-3 5 6-2 2"/><path d="m19 12-1 3h3z"/></symbol>
  <symbol id="i-headset" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 18v-6a9 9 0 0 1 18 0v6"/><path d="M21 19a2 2 0 0 1-2 2h-1v-6h3zM3 19a2 2 0 0 0 2 2h1v-6H3z"/></symbol>
  <symbol id="i-star" viewBox="0 0 24 24" fill="currentColor"><path d="m12 2 3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z"/></symbol>
  <symbol id="i-fb" viewBox="0 0 24 24" fill="currentColor"><path d="M14 8.5V6.8c0-.8.2-1.3 1.4-1.3H17V2.2c-.3 0-1.3-.1-2.5-.1-2.5 0-4.2 1.5-4.2 4.3v2.1H7.5V12h2.8v10H14V12h2.8l.4-3.5z"/></symbol>
  <symbol id="i-g" viewBox="0 0 48 48"><path fill="#FFC107" d="M43.6 20.1H42V20H24v8h11.3C33.7 32.7 29.2 36 24 36c-6.6 0-12-5.4-12-12s5.4-12 12-12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 12.9 4 4 12.9 4 24s8.9 20 20 20 20-8.9 20-20c0-1.3-.1-2.6-.4-3.9z"/><path fill="#FF3D00" d="m6.3 14.7 6.6 4.8C14.7 15.1 19 12 24 12c3.1 0 5.8 1.2 7.9 3.1l5.7-5.7C34 6.1 29.3 4 24 4 16.3 4 9.7 8.3 6.3 14.7z"/><path fill="#4CAF50" d="M24 44c5.2 0 9.9-2 13.4-5.2l-6.2-5.2A11.9 11.9 0 0 1 24 36c-5.2 0-9.6-3.3-11.3-8l-6.5 5C9.5 39.6 16.2 44 24 44z"/><path fill="#1976D2" d="M43.6 20.1H42V20H24v8h11.3a12 12 0 0 1-4.1 5.6l6.2 5.2C36.9 39.2 44 34 44 24c0-1.3-.1-2.6-.4-3.9z"/></symbol>
  <symbol id="i-logo" viewBox="0 0 177.017 76.773">""" + LOGO_INNER + """</symbol>
</svg>"""

def ic(name, cls="icon"):
    return f'<svg class="{cls}" aria-hidden="true"><use href="#i-{name}"/></svg>'

LOGO_SVG = '<svg viewBox="0 0 177.017 76.773" role="img" aria-label="Northland Plumbing, Gas &amp; Drainage"><use href="#i-logo"/></svg>'
G = '<svg class="g" viewBox="0 0 48 48" aria-hidden="true"><use href="#i-g"/></svg>'
STARS5 = '<span class="stars" aria-hidden="true">★★★★★</span>'
STARS45 = '<span class="stars" aria-hidden="true">★★★★<span style="opacity:.45">★</span></span>'

# ---------------------------------------------------------------- services
SERVICES = [
    dict(slug="plumbing", title="Plumbing", tile="plumbing-bathroom-vanity",
         blurb="New homes, renovations, leaks, blocked drains and fit-offs, done by qualified plumbers.",
         h1="Plumbing for Northland homes", eyebrow="Residential plumbing",
         lead="From new-build pipe-outs to a leaking tap on a Sunday-best bathroom, our qualified plumbers handle the lot across Whangārei and Northland.",
         list=["New home plumbing and hot water systems", "Renovation plumbing, kitchen and bathroom refits", "Gas and electric hot water supply and install", "Emergency repairs: burst pipes, leaks, blocked drains", "Water purification and filtration systems", "Wet-back fire hot water systems", "Drain camera inspections and backflow prevention"],
         body=["Northland Plumbing, Gas & Drainage looks after both homes and businesses. That covers new home plumbing, hot water installs, fixing leaking pipes and clearing blocked drains, right through to commercial installs and kitchen fit-outs.",
               "Renovating? Our team can upgrade an outdated system or plumb a new kitchen or bathroom from start to finish, and we supply and install gas califonts and electric hot water cylinders sized to how you actually use water.",
               "We also supply and install water filtration and purification systems for clean drinking water, wet-back fire hot water systems and solar water heating, and we use camera inspections to find drainage faults without guesswork."],
         photos=["shower-install", "outdoor-tap", "bathroom-renovation"],
         faq=[("Can you plumb our renovation from start to finish?", "Yes. Our plumbers handle renovation plumbing for kitchens and bathrooms, and if the job needs gas, drainage or a new hot water system, the same team can do that too."),
              ("Do you install water filters?", "Yes. We supply and install water purification and filtration systems for homes and businesses. Call us to talk through what suits your supply, whether that's town water or tank water."),
              ("Can you find a leak or blockage without digging everything up?", "We use drain camera inspections to see what is going on inside your pipes before deciding on a fix.")]),
    dict(slug="gas-fitting", title="Gas fitting", tile="gas-hob-install",
         blurb="Gas hobs, califonts, heating and full commercial kitchen fit-outs, certified and signed off.",
         h1="Certified gas fitting", eyebrow="Gas fitting, home and commercial",
         lead="Gas hobs, ovens, califonts and gas heating, installed safely and certified by registered gasfitters. 0800 WANT GAS is our number for a reason.",
         list=["Gas hob installations and replacements", "Gas califont installations and replacements", "Gas ovens and gas heating", "Gas fires and outdoor gas connections", "Commercial kitchen gas fit-outs", "Commercial gas appliance repairs, boilers and large gas water systems", "Certification of new and existing gas systems"],
         body=["Our gasfitters install, replace and repair gas hobs, ovens, califonts and gas heating, and every installation is completed safely and certified to the required standards.",
               "For businesses we handle full commercial kitchen gas fit-outs for restaurants and cafes, plus repairs on commercial gas appliances, boilers and large-scale gas water systems.",
               "Not sure an old installation is safe? We regularly come across non-compliant work, like LPG bottles stored inside or too close to power points. Get it checked and certified."],
         photos=["control-panel", "outdoor-califonts", "maintenance-connection"],
         faq=[("Will I get a gas certificate?", "Yes. Gas installations are completed by registered gasfitters and certified, with full sign-off when the job is done."),
              ("Can you swap my electric cooktop for gas?", "Yes, we install gas hobs and ovens. Electrical work, such as disconnecting the old cooktop, may need an electrician; ask us when you call."),
              ("Do you do commercial kitchens?", "Yes. We fit out commercial kitchens with gas and plumbing and repair commercial gas appliances.")]),
    dict(slug="hot-water", title="Hot water", tile="hot-water-rinnai",
         blurb="Gas califonts, electric cylinders, mains pressure upgrades and wet-backs. Supplied, installed, certified.",
         h1="Hot water that lasts the distance", eyebrow="Hot water systems",
         lead="Instant gas, mains pressure electric, wet-back or solar. We supply, install, repair and certify hot water systems for homes, farms and businesses.",
         list=["New home gas hot water systems", "New home electric hot water systems", "Califont and push-through water heating", "Repairs to gas water heaters, califonts and continuous flow units", "Wood fire wet-back systems", "Commercial and industrial boilers", "Certification of new and existing gas water heating"],
         body=["Building new, replacing a tired cylinder or sick of the shower going cold? Our gasfitters and plumbers will recommend the right system for your property and how you use hot water, then supply, install and certify it.",
               "We install gas califonts for continuous hot water, electric mains pressure cylinders, wood fire wet-backs and more, and we repair gas water heaters and califonts when they play up.",
               "We also look after commercial and industrial boilers, from installation through to repairs and ongoing maintenance, and we are a Rheem service agent."],
         photos=["hero-hot-water-install", "outdoor-califonts", "control-panel"],
         faq=[("Gas califont or electric cylinder?", "It depends on your gas supply, how many people are in the house and where the unit can go. Califonts give continuous hot water; mains pressure cylinders give strong pressure from stored water. We will talk you through it."),
              ("What is in the hot water deals?", "Right now: a Rinnai A26 gas califont conversion for $3,200 incl GST, or a Dux mains pressure electric cylinder upgrade for $2,950 incl GST. Electrical work is not included and terms apply."),
              ("Can you fix my califont rather than replace it?", "Often, yes. We repair gas water heaters, califonts and continuous flow units, and we will tell you straight if replacing makes more sense.")]),
    dict(slug="drainlaying", title="Drainlaying", tile="drainage-site",
         blurb="Certified drainlayers for new homes, subdivisions, commercial sites and stubborn blocked drains.",
         h1="Drainlaying done right the first time", eyebrow="Certified drainlayers",
         lead="Our drainlayers are qualified and certified by the Plumbers, Gasfitters and Drainlayers Board, with the gear to get your project in on time and on budget.",
         list=["New residential home drainlaying", "Wastewater reports for building consent", "New commercial and industrial drainlaying", "Septic tank installations", "Stormwater and drainage systems", "Certifying drainlayer services", "Blocked drains and drain cleaning"],
         body=["Getting drainage right matters. Our Whangārei drainlayers design and install drainage, prepare the wastewater reports required at building consent, and deliver treatment and water harvesting systems built to last.",
               "Because we do the drainlaying, the earthworks and the plumbing, we can take a project from the first trench right through to the final plumbing fit-out. Fewer trades to chase, less downtime.",
               "Got drains that keep blocking? We clear blocked drains, fix leaking pipes and find the cause, so you are not calling someone back every few months."],
         photos=["drain-trench", "septic-tank-crane", "wastewater-tanks"],
         faq=[("Do I need a wastewater report for my building consent?", "Many rural and lifestyle sites do. We prepare wastewater reports for building consent applications. Talk to us before you submit your plans; good planning early can save money."),
              ("Are your drainlayers certified?", "Yes. Our drainlayers are qualified and certified by the New Zealand Plumbers, Gasfitters and Drainlayers Board, and we offer certifying drainlayer services."),
              ("Can you do the digging as well?", "Yes. We run our own diggers, so trenching, drainlaying and backfill are handled by one team.")]),
    dict(slug="wastewater", title="Wastewater systems", tile="wastewater-tanks",
         blurb="Septic tanks and treatment systems designed for your site, from consent report to commissioning.",
         h1="Wastewater systems for rural Northland", eyebrow="Septic and wastewater",
         lead="Septic tanks, aerated treatment plants and pressure sewer systems, designed around your site and Northland's ground conditions.",
         list=["Wastewater design and planning", "Wastewater reports for building consent", "Septic tank installation", "Aerated and secondary treatment systems", "Pressure sewer and grinder pump systems", "Water harvesting and storage"],
         body=["We design, install and look after wastewater systems throughout Northland. Our local team knows the region's soils and conditions, so your system is designed to treat wastewater properly, protect the environment and meet council requirements.",
               "Talk to us at the planning stage. We can prepare the wastewater report for your building consent, recommend the right system for your section and then install it, with the earthworks, drainlaying and plumbing all done by one crew."],
         brands=[("econo-treat.svg", "Econo-Treat", "A cost-effective aerated sewage treatment system that runs on low power, in plastic or concrete tanks and a range of capacities."),
                 ("naturalflow.svg", "NaturalFlow", "Sustainable, odourless modular wastewater systems for homes and businesses, designed for your specific site from primary to secondary treatment."),
                 ("duracrete.png", "Duracrete CleanStream TXR", "An advanced secondary treatment system for homes that is reliable, robust and cost effective to run and service."),
                 ("e-one.png", "E/One pressure sewer", "Small-diameter pipes and a grinder pump station that turns household wastewater into a slurry and pumps it to the main or a treatment plant."),
                 ("aquatec.png", "Aquatec pressure sewer", "A pressure sewer system tailored to your site's conditions for an economical, reliable result.")],
         photos=["septic-tank-crane", "drain-trench", "drainage-site"],
         faq=[("Which treatment system is right for my property?", "It depends on your soil, section size, household size and council rules. We will look at your site and recommend a system, then design and install it."),
              ("Can you handle the consent side?", "We prepare wastewater reports for building consent applications. Getting us involved before you lodge plans usually saves time and money."),
              ("Do you install the tanks as well as design the system?", "Yes. We do the earthworks, tank installation, drainlaying and plumbing, so one team owns the whole job.")]),
    dict(slug="excavation-earthworks", title="Excavation & earthworks", tile="earthworks-diggers",
         blurb="Site clearing, levelling, trenching, cut and fill, driveways and retaining. Our own diggers, our own operators.",
         h1="Excavation and earthworks", eyebrow="Diggers, trucks, qualified operators",
         lead="Site prep, trenching, bulk earthworks and clean-ups for homes, farms and commercial sites. Our qualified operators and our own machines.",
         list=["Site preparation, clearing and levelling", "Trenching for services, drainage and foundations", "Bulk earthworks, cut and fill", "Driveways, retaining walls and landscaping", "Demolition and site clean-up", "Urgent earthmoving, such as flood clean-ups", "Residential digger and excavator hire"],
         body=["Excavation done right from the start saves trouble later. We prepare building sites, clear and level land, dig trenches for drainage, services and foundations, and move bulk earth for residential, commercial and industrial projects.",
               "Our digger operators are fully qualified, and because we also do the drainage and plumbing, the trenches get dug, laid and backfilled by one team with minimal downtime.",
               "Need a driveway formed, a retaining wall built or a site cleaned up after demolition or flooding? Give us a call."],
         photos=["earthworks-diggers", "drain-trench", "drainage-site"],
         faq=[("Do you hire out diggers with an operator?", "Yes. Our residential digger and excavator hire comes with a qualified operator."),
              ("Can you help after a flood or slip?", "We are available for urgent earthmoving such as flood damage clean-ups. Call us and tell us what you are dealing with."),
              ("Do I need consent for earthworks?", "Some jobs do. Ask us when you call and we will explain what applies to your site.")]),
    dict(slug="underfloor-heating", title="Underfloor heating", tile="underfloor-pipes",
         blurb="Hot water floor heating designed into your new build and warming the whole home from the ground up.",
         h1="Underfloor heating", eyebrow="Hot water floor heating",
         lead="Warm the whole house evenly from the floor up, with piped hot water heating designed for your new build.",
         list=["New residential hot water floor heating", "Underfloor heating for commercial and industrial projects", "Piped systems customised to your new build", "Design, supply, install and certification"],
         body=["Hot water floor heating warms an entire home or building evenly and economically from the floor up, and it is invisible: no radiators or heat pump heads on the walls.",
               "Unlike a wood burner or radiator that heats one or two rooms, floor heating warms the whole home. We design, supply, install and certify the full system for new residential and commercial builds.",
               "Talk to us early in the planning stage of your build so the system can be designed in properly and give you the best value."],
         photos=["underfloor-pipes", "hero-van-new-build", "plumbing-bathroom-vanity"],
         faq=[("When should I talk to you about underfloor heating?", "As early as possible in the planning stage of your build, so pipes can be laid before the slab is poured."),
              ("Can it go in an existing house?", "Our floor heating is designed for new builds. Call us to talk through your options."),
              ("Do you do commercial floor heating?", "Yes, for commercial and industrial projects as well as homes.")]),
    dict(slug="commercial-plumbing", title="Commercial plumbing & gas", tile="commercial-bathrooms",
         blurb="Shops, schools, kitchens and civic buildings. Designed, installed, certified and maintained with minimal downtime.",
         h1="Commercial plumbing and gas", eyebrow="Commercial and industrial",
         lead="Plumbing and gas for businesses, shops, schools, hospitals and civic buildings, delivered on deadline with full certification and sign-off.",
         list=["Supply and installation of plumbing systems", "Supply, installation and certification of gas systems", "Commercial kitchen plumbing, gas fitting and refits", "Industrial and commercial heating", "Commercial gas and hot water repair and maintenance", "Scheduled plumbing and gas servicing"],
         body=["We supply and install plumbing, hot water and commercial gas systems through to full certification, and we can help design the right system for efficient, cost-effective running.",
               "We have worked on plumbing and gas projects in New Zealand and Australia, so we know how much downtime costs a business. Our teams work to project deadlines and keep plant down-time to a minimum.",
               "All work is completed by qualified and registered plumbers, gasfitters and drainlayers, with full certification and legal sign-off at the end of the job."],
         photos=["commercial-bathrooms", "hot-water-rinnai", "team-in-van"],
         faq=[("Can you work around our opening hours?", "We understand downtime costs money and plan work to keep disruption to a minimum. Talk to us about timing when you book."),
              ("Do you offer maintenance contracts?", "We offer scheduled, regular plumbing and gas system servicing for businesses."),
              ("Do you handle certification and sign-off?", "Yes. You get full certification and legal sign-off when the project is complete.")]),
    dict(slug="repairs-maintenance", title="Repairs & maintenance", tile="maintenance-connection",
         blurb="Leaks, no hot water, gas faults and scheduled servicing. Fast, fair-priced and done properly.",
         h1="Repairs and maintenance", eyebrow="Plumbing, gas and hot water repairs",
         lead="Leaking pipe, no hot water or a gas appliance playing up? Call our team and we will get your system running again.",
         list=["Quick, efficient plumbing repairs and maintenance", "Fast gas system repairs and maintenance", "Urgent plumbing and gas repairs", "Hot water system repairs", "Scheduled gas and plumbing servicing"],
         body=["Our plumbers, gasfitters and drainlayers are based in Whangārei and get homes and businesses up and running again quickly, at a fair price.",
               "Hot water trouble? We repair hot water systems and look after them with regular maintenance. The faster a fault is fixed, the less damage and lost time it causes.",
               "Our office is open Monday to Friday, 8am to 4.30pm. Call 0800 WANT GAS to book a repair or set up scheduled servicing."],
         photos=["maintenance-connection", "toolbox-van", "coil-van"],
         faq=[("How fast can you get to me?", "Call 0800 WANT GAS and tell us what is going on. We will give you a straight answer on timing when you call."),
              ("Do you take small jobs?", "Yes. Customers tell us we are one of the few teams that will turn up for the small stuff, like a leaking tap or a dripping valve."),
              ("Can you service my gas appliances regularly?", "Yes. We offer scheduled gas and plumbing system servicing.")]),
    dict(slug="water-delivery", title="Water delivery", tile="water-truck-pool",
         blurb="Up to 10,000 litres of drinking water per load, from a Taumata Arowai registered water carrier.",
         h1="Fresh water delivered", eyebrow="0800 WANT H2O",
         lead="Running low? Our tankers carry up to 10,000 litres of fresh, potable water to homes across Whangārei and Dargaville districts.",
         list=["Tank top-ups and full tank fills", "Swimming pool fills", "Up to 10,000 litres per load", "Taumata Arowai registered water carrier", "Whangārei and Dargaville delivery zones", "Flexible scheduling, clear no-obligation quotes"],
         body=["Whether you are topping up the tank, filling a pool or getting ready for a dry summer, we will get you the water you need without the stress.",
               "Northland Plumbing, Gas & Drainage is a Taumata Arowai registered water carrier, so the water we deliver is clean, safe, potable water suitable for drinking, pools and storage tanks.",
               "Prices are based on your delivery zone and accessible delivery. Hard to reach? Tell us and we will do our best to make it work."],
         photos=["water-truck-filling", "water-truck-shed", "water-truck-pool"],
         faq=[("Is the water safe to drink?", "Yes. We are a Taumata Arowai registered water carrier and supply only clean, potable water."),
              ("How much water can you deliver?", "Our tankers carry up to 10,000 litres per load."),
              ("Where do you deliver?", "Throughout the Whangārei district and the Dargaville area. Check the delivery zone maps or call 0800 WANT H2O.")]),
]
SVC = {s["slug"]: s for s in SERVICES}

REVIEWS = [
    ("Kelli Booth", "2026", "Gas fire repair", "Fantastic service, we had quite a tricky job on an old gas fire. Mike managed to sort it and saved us potentially $1000’s on needing a brand new replacement. … Their costings are transparent so you know exactly what to expect. A really professional and nice bunch of guys. Highly recommended."),
    ("Camden Andrews", "2024", "New build", "Hamish and his team have completed the plumbing and drainage on our new build in Northland and we cannot recommend them enough. Very approachable and professional with an extremely high level of workmanship and attention to detail."),
    ("John Haselden", "2023", "Hot water repair", "Our very old (first floor) hot water system emptied itself overnight through the lower level bathroom ceiling. NP's response was quick, job was assessed and repairs scheduled. Alterations were also made to modernise to latest standards to ensure this could never happen again. … Overall outstanding service."),
    ("Vijay Harypursat", "2023", "Califont replacement", "Our califont got flooded and died, and I called around to try and have it replaced. Hamish responded immediately with a phone call, and then came over to have a look. Gene came over a couple of days later and efficiently installed a new califont and controller. Thanks guys for the effort and great work!!"),
    ("Paula Horsley", "2023", "Leak repair", "I was really impressed with how quickly the job was attended to as it is becoming difficult to find trades that will attend smaller jobs. The job was completed in a timely manner and to a high standard. I was given a detailed explanation of the issue and how it would be fixed."),
    ("Aklesha Morrison", "2024", "Plumbing", "Callum was awesome from the start. Went out of his way to make it as cheap as possible and explained everything in layman terms. Would definitely recommend this company to anyone!"),
]

HOME_FAQ = [
    ("What areas do you cover?", "We are based at 140 Lower Dent Street in Whangārei and work right across Northland. Water delivery runs in set zones around Whangārei and Dargaville; see the <a href=\"services/water-delivery.html\">delivery maps</a>."),
    ("How do I get a quote?", "Call 0800 WANT GAS (0800 926 8427) or email info&#64;northlandpg.co.nz with the address and what you need done. For new builds and renovations, get in touch at the planning stage; we can usually save you money with good planning early."),
    ("Can one company really do the whole job?", "Yes. We do the earthworks, drainlaying, wastewater, plumbing, gas and hot water, so a new build or rural section can go from first trench to final fit-off with one team and one point of contact."),
    ("Do you prepare wastewater reports for building consent?", "Yes. Wastewater reports are often required with a building consent application for rural sites. Talk to us before you submit plans to council."),
    ("Are your people qualified?", "Our plumbers, gasfitters and drainlayers are qualified and registered, our drainlayers are certified by the Plumbers, Gasfitters and Drainlayers Board, and gas work is certified and signed off. We are Master Plumbers members and hold Sitewise Gold for 2025/26."),
    ("What is included in the hot water deals?", "The Rinnai A26 conversion ($3,200 incl GST) replaces your old cylinder with instant gas hot water. The mains pressure upgrade ($2,950 incl GST) supplies and installs an electric mains pressure cylinder with valves, seismic restraints, tempering valve and removal of the old cylinder, connected to existing plumbing in the same location. Electrical work is not included and terms apply."),
    ("Is your delivered water safe to drink?", "Yes. We are a Taumata Arowai registered water carrier and deliver clean, potable water, up to 10,000 litres per load."),
    ("What are your hours?", "Our office is open Monday to Friday, 8am to 4.30pm. Call 0800 WANT GAS to book a job, or 0800 WANT H2O for water delivery."),
]

GALLERY = [
    ("drain-trench", "Drainage trench, rural Northland"),
    ("hero-hot-water-install", "Hot water system install"),
    ("septic-tank-crane", "Septic tanks going in"),
    ("shower-install", "Shower fit-off"),
    ("outdoor-califonts", "Outdoor gas califonts"),
    ("earthworks-diggers", "Earthworks and site prep"),
    ("bathroom-renovation", "Bathroom renovation"),
    ("wastewater-tanks", "Treatment system install"),
    ("van-coast", "On the road, Northland"),
]

# ---------------------------------------------------------------- shared chrome
NAV_ITEMS = [("Services", "#services"), ("Hot water deals", "#deals"), ("Water delivery", "#water"), ("About", "#about"), ("Reviews", "#reviews"), ("FAQ", "#faq"), ("Contact", "#contact")]

def head(title, desc, canonical, prefix="", og_img="img/og-image.jpg", extra_ld=""):
    return f"""<!DOCTYPE html>
<html lang="en-NZ">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{SITE_URL}/{canonical}">
<meta name="theme-color" content="#061a2c">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{e(NAME)}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{SITE_URL}/{canonical}">
<meta property="og:image" content="{SITE_URL}/{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{prefix}favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{prefix}img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@700;800;900&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{prefix}styles.css">
<script>document.documentElement.classList.add('js')</script>
{extra_ld}</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{ICONS}
"""

def ribbon(prefix):
    return f'<div class="ribbon"><span class="rl">Hot water deal: </span>instant gas hot water with a Rinnai A26, $3,200 incl GST. <a href="{prefix}index.html#deals">See the deals</a></div>\n'

def nav(prefix, current=None, sub=False, solid=False):
    items = []
    for label, href in NAV_ITEMS:
        h = (prefix + "index.html" + href) if (prefix or sub) else href
        cur = ' aria-current="page"' if current == label else ""
        items.append(f'<li><a href="{h}"{cur}>{label}</a></li>')
    home = prefix + "index.html" if (prefix or sub) else "#top"
    cls = "nav solid" if solid else "nav"
    return f"""<header class="{cls}" id="nav">
  <div class="wrap">
    <a href="{home}" class="logo" aria-label="Northland Plumbing, Gas &amp; Drainage home">{LOGO_SVG}</a>
    <ul class="nav-links" id="navLinks">
      {''.join(items)}
    </ul>
    <div class="nav-right">
      <a class="btn btn-primary nav-call" href="{GAS_TEL}">{ic('phone')}<span class="label">{GAS_TXT}</span></a>
      <button class="burger" id="burger" aria-label="Open menu" aria-expanded="false" aria-controls="navLinks">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="square"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
      </button>
    </div>
  </div>
</header>
"""

def contact_section(prefix, heading="Got a job? Let's talk.", sub="Call for a quote or email us the details. Talk to us early on new builds and renovations; good planning saves money."):
    mail = gmail("Job enquiry", "Hi Northland Plumbing, Gas & Drainage,\n\nI'd like a quote for:\n\nJob address:\n\nBest number to reach me:\n\nThanks")
    return f"""<section id="contact" class="contact">
  <div class="wrap contact-grid">
    <div>
      <span class="eyebrow reveal">Contact</span>
      <h2 class="reveal">{heading}</h2>
      <p class="muted reveal">{sub}</p>
      <ul class="contact-rows reveal">
        <li>{ic('phone')}<div><a href="{GAS_TEL}">{GAS_TXT} &middot; {GAS_DIGITS}</a><small>Plumbing, gas, drainage and earthworks</small></div></li>
        <li>{ic('drop')}<div><a href="{H2O_TEL}">{H2O_TXT} &middot; {H2O_DIGITS}</a><small>Water delivery</small></div></li>
        <li>{ic('headset')}<div><a href="{ADMIN_TEL}">{ADMIN_TXT}</a><small>Office and accounts</small></div></li>
        <li>{ic('mail')}<div><a href="{mail}" target="_blank" rel="noopener">{EMAIL_TEXT}</a></div></li>
        <li>{ic('pin')}<div><a href="{MAPS}" target="_blank" rel="noopener">{ADDRESS}</a><small>Postal: PO Box 11011, Te Mai Mail Centre, Whangārei</small></div></li>
        <li>{ic('clock')}<div>Monday to Friday, 8am to 4.30pm<small>Weekends closed</small></div></li>
      </ul>
      <div class="socials reveal">
        <a href="{FB}" target="_blank" rel="noopener" aria-label="Northland Plumbing, Gas &amp; Drainage on Facebook">{ic('fb', '')}</a>
      </div>
    </div>
    <div class="contact-actions">
      <a class="btn btn-primary reveal" href="{GAS_TEL}"><span>Call for a quote<small>{GAS_TXT} &middot; {GAS_DIGITS}</small></span>{ic('phone')}</a>
      <a class="btn btn-ghost reveal" href="{mail}" target="_blank" rel="noopener"><span>Email us the job<small>Opens a pre-filled email</small></span>{ic('mail')}</a>
      <a class="btn btn-ghost reveal" href="{H2O_TEL}"><span>Order water<small>{H2O_TXT} &middot; {H2O_DIGITS}</small></span>{ic('truck')}</a>
    </div>
  </div>
</section>
"""

def map_section():
    return f"""<section class="map" aria-label="Map">
  <iframe title="Map to Northland Plumbing, Gas &amp; Drainage, 140 Lower Dent Street, Whangārei" src="{MAP_EMBED}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
</section>
"""

def footer(prefix):
    svc_links = "".join(f'<li><a href="{prefix}services/{s["slug"]}.html">{s["title"]}</a></li>' for s in SERVICES[:6])
    svc_links2 = "".join(f'<li><a href="{prefix}services/{s["slug"]}.html">{s["title"]}</a></li>' for s in SERVICES[6:])
    return f"""<footer class="footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <a href="{prefix}index.html" class="logo" aria-label="Home">{LOGO_SVG}</a>
        <p style="margin-top:18px">Plumbers, gasfitters, drainlayers and earthworks from Whangārei, working right across Northland.</p>
        <div class="badges">
          <img src="{prefix}img/brands/logo-master-plumbers.png" alt="Master Plumbers member" width="420" height="150" loading="lazy">
          <img src="{prefix}img/brands/logo-sitewise-gold-2025.png" alt="Sitewise Gold 2025/2026" width="440" height="160" loading="lazy">
        </div>
      </div>
      <div><h4>Services</h4><ul>{svc_links}</ul></div>
      <div><h4>More</h4><ul>{svc_links2}<li><a href="{prefix}index.html#deals">Hot water deals</a></li><li><a href="{JOB_AD}" target="_blank" rel="noopener">Careers</a></li></ul></div>
      <div><h4>Get in touch</h4><ul>
        <li><a href="{GAS_TEL}">{GAS_TXT}</a></li>
        <li><a href="{H2O_TEL}">{H2O_TXT}</a></li>
        <li><a href="{gmail('Enquiry', 'Hi team,')}" target="_blank" rel="noopener">{EMAIL_TEXT}</a></li>
        <li>{ADDRESS}</li>
        <li><a href="{FB}" target="_blank" rel="noopener">Facebook</a></li>
      </ul></div>
    </div>
    <div class="footer-bottom">
      <span>&copy; <span id="year">2026</span> {NAME} &middot; Whangārei, Northland</span>
      <span><a href="{prefix}privacy.html">Privacy</a> &middot; <a href="{prefix}terms.html">Terms</a> &middot; <a href="{G_WRITE}" target="_blank" rel="noopener">Leave a Google review</a></span>
    </div>
  </div>
</footer>
<nav class="callbar" aria-label="Quick contact">
  <a class="c1" href="{GAS_TEL}">{ic('phone', '')}Call now</a>
  <a class="c2" href="{prefix}index.html#contact">{ic('mail', '')}Get a quote</a>
</nav>
<script src="{prefix}app.js"></script>
</body>
</html>
"""

def faq_html(items):
    return "\n".join(f"      <details><summary>{e(qn)}</summary><p>{a}</p></details>" for qn, a in items)

LD_BUSINESS = {
    "@context": "https://schema.org", "@type": "Plumber", "name": NAME, "url": SITE_URL + "/",
    "telephone": "+64 800 926 8427", "email": f"{EMAIL_USER}@{EMAIL_DOMAIN}",
    "image": SITE_URL + "/img/og-image.jpg", "logo": SITE_URL + "/favicon.svg",
    "address": {"@type": "PostalAddress", "streetAddress": "140 Lower Dent Street", "addressLocality": "Whangārei", "postalCode": "0110", "addressRegion": "Northland", "addressCountry": "NZ"},
    "geo": {"@type": "GeoCoordinates", "latitude": -35.7273589, "longitude": 174.3290948},
    "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "08:00", "closes": "16:30"}],
    "areaServed": "Northland, New Zealand", "sameAs": [FB],
    "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Services", "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["title"]}} for s in SERVICES]},
}

# ---------------------------------------------------------------- homepage
def home():
    tiles_layout = ["wide", "", "", "", "", "", "wide", "", "", ""]
    tiles = []
    for i, (s, lay) in enumerate(zip(SERVICES, tiles_layout)):
        sizes = "(max-width:600px) 100vw, (max-width:900px) 100vw, 66vw" if lay else "(max-width:600px) 100vw, (max-width:900px) 50vw, 33vw"
        tiles.append(f'''      <a href="services/{s["slug"]}.html" class="tile {lay} wipe">{pic(s["tile"], s["title"], sizes)}<div class="tile-body"><span class="num">{i+1:02d}</span><h3>{s["title"]}</h3><p>{s["blurb"]}</p><span class="more">Learn more {ic("arrow", "")}</span></div></a>''')
    reviews = []
    for n, yr, job, txt in REVIEWS:
        reviews.append(f'''      <figure class="review reveal"><div class="review-top">{STARS5}<svg class="g" viewBox="0 0 48 48" aria-label="Google review"><use href="#i-g"/></svg></div><blockquote>“{e(txt)}”</blockquote><footer><div><strong>{e(n)}</strong>{job} &middot; {yr}</div></footer></figure>''')
    gallery = "\n".join(f'''      <figure class="wipe-up">{pic(n, c, "(max-width:520px) 100vw, (max-width:900px) 50vw, 33vw", extra=f' data-full="img/{n}-1920.webp"')}<figcaption>{c}</figcaption></figure>''' for n, c in GALLERY)
    brands = ["rheem.svg", "rockgas-north.png", "plumbing-world.png", "waterflow.png", "obriens.png", "duracrete.png", "econo-treat.svg", "naturalflow.svg", "e-one.png", "aquatec.png", "ecodan.png", "black-diamond.png"]
    names = {"rheem.svg": "Rheem", "rockgas-north.png": "Rockgas North", "plumbing-world.png": "Plumbing World", "waterflow.png": "Water Flow NZ", "obriens.png": "O'Briens Plumbing and Bathroomware", "duracrete.png": "Duracrete", "econo-treat.svg": "Econo-Treat", "naturalflow.svg": "NaturalFlow", "e-one.png": "E/One", "aquatec.png": "Aquatec", "ecodan.png": "Ecodan", "black-diamond.png": "Black Diamond"}
    def brand_ul(hidden):
        hid = ' aria-hidden="true"' if hidden else ""
        return (f'<ul{hid}>' + "".join(f'<li><img src="img/brands/logo-{b}" alt="{"" if hidden else e(names[b])}" loading="lazy"></li>' for b in brands) + "</ul>")
    mail_deal = gmail("Hot water deal enquiry", "Hi team,\n\nI'm interested in the hot water deal:\n\nAddress:\n\nCurrent hot water system:\n\nThanks")
    import re
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": qn, "acceptedAnswer": {"@type": "Answer", "text": html.unescape(re.sub("<[^>]+>", "", a))}} for qn, a in HOME_FAQ]}
    ld = ('<script type="application/ld+json">' + json.dumps(LD_BUSINESS, ensure_ascii=False) + '</script>\n'
          '<script type="application/ld+json">' + json.dumps(faq_ld, ensure_ascii=False) + '</script>\n')
    out = head("Northland Plumbing, Gas & Drainage | Plumbers, Gasfitters & Drainlayers, Whangārei",
               "Whangārei plumbers, gasfitters and certified drainlayers with our own diggers and water tankers. Plumbing, gas, hot water, wastewater, earthworks and water delivery across Northland. Call 0800 WANT GAS.",
               "", extra_ld=ld)
    out += ribbon("") + nav("")
    out += f"""
<main id="main">
<span id="top"></span>

<!-- HERO -->
<section class="hero" aria-label="Introduction">
  <div class="hero-slides" id="heroSlides">
    {pic("hero-team-aerial", "The Northland Plumbing, Gas & Drainage crew and fleet", "100vw", "active", eager=True, hero=True)}
    {pic("hero-van-new-build", "Northland Plumbing van outside a new build", "100vw", hero=True)}
    {pic("hero-excavator", "Our excavator on a drainage job", "100vw", hero=True)}
    {pic("hero-hot-water-install", "Plumber installing a hot water system", "100vw", hero=True)}
  </div>
  <div class="wrap">
    <span class="eyebrow hero-fade">Whangārei based &middot; Northland wide</span>
    <h1>
      <span class="line"><span>Plumbing, gas</span></span>
      <span class="line"><span>&amp; drainage for</span></span>
      <span class="line"><span class="hl">all of Northland</span></span>
    </h1>
    <div class="hero-bottom hero-fade">
      <div>
        <p class="lead">Qualified plumbers, gasfitters and certified drainlayers with our own diggers and water tankers. One local crew, from the first trench to the final fit-off.</p>
        <div class="hero-ctas">
          <a class="btn btn-primary" href="{GAS_TEL}">{ic('phone')}Call {GAS_TXT}</a>
          <a class="btn btn-ghost" href="#contact">Get a quote {ic('arrow')}</a>
        </div>
      </div>
      <div class="ratings">
        <a class="rating" href="{G_REVIEWS}" target="_blank" rel="noopener" aria-label="Rated 4.5 out of 5 from 77 Google reviews">
          {G}<span class="num">4.5</span><div>{STARS45}<small>77 Google reviews</small></div>
        </a>
      </div>
    </div>
    <div class="slide-dots hero-fade" id="dots" aria-hidden="true"><span class="on"></span><span></span><span></span><span></span></div>
  </div>
</section>

<!-- TRUST STRIP -->
<section class="trust" aria-label="Why choose us">
  <div class="wrap trust-grid">
    <div class="trust-item">{ic('award')}<div><strong>Master Plumbers</strong><span>Member of Master Plumbers NZ</span></div></div>
    <div class="trust-item">{ic('shield')}<div><strong>Sitewise Gold</strong><span>Health and safety, 2025/26</span></div></div>
    <div class="trust-item">{ic('check')}<div><strong>Certified &amp; registered</strong><span>Plumbers, gasfitters, drainlayers</span></div></div>
    <div class="trust-item">{ic('flame')}<div><strong>Rheem service agent</strong><span>Hot water serviced properly</span></div></div>
  </div>
</section>

<!-- SERVICES -->
<section id="services" class="band-dark">
  <div class="wrap">
    <div class="section-head">
      <div><span class="eyebrow reveal">What we do</span><h2 class="reveal">Ten trades. One crew.</h2></div>
      <p class="muted reveal">Plumbing, gas, hot water, drainage, wastewater and earthworks, plus water delivery. Tap any service for the details.</p>
    </div>
    <div class="tiles">
{chr(10).join(tiles)}
    </div>
  </div>
</section>

<!-- DEALS -->
<section id="deals" class="band-mist">
  <div class="wrap">
    <div class="section-head">
      <div><span class="eyebrow reveal">Current hot water deals</span><h2 class="reveal">Better hot water, one fixed price</h2></div>
      <p class="muted reveal">Supply and installation by our certified gasfitters and plumbers. Prices include GST.</p>
    </div>
    <div class="deals-grid">
      <article class="deal reveal">
        <div class="deal-img">{pic("hot-water-rinnai", "Rinnai gas califont installed on a wall", "(max-width:600px) 100vw, 25vw")}</div>
        <div class="deal-body">
          <span class="tag">Instant gas hot water</span>
          <h3>Rinnai A26 califont conversion</h3>
          <div class="price">$3,200<small>incl GST</small></div>
          <ul>
            <li>{ic('check', '')}Convert your old hot water cylinder to instant, continuous gas hot water</li>
            <li>{ic('check', '')}Rinnai A26 califont supplied and installed</li>
          </ul>
          <p class="fine">Electrical work not included. Terms and conditions apply.</p>
          <a class="btn btn-primary" href="{GAS_TEL}">{ic('phone')}Book this deal</a>
        </div>
      </article>
      <article class="deal reveal">
        <div class="deal-img">{pic("hero-hot-water-install", "Plumber installing a hot water system", "(max-width:600px) 100vw, 25vw")}</div>
        <div class="deal-body">
          <span class="tag">Mains pressure</span>
          <h3>Mains pressure cylinder upgrade</h3>
          <div class="price">$2,950<small>incl GST</small></div>
          <ul>
            <li>{ic('check', '')}Electric mains pressure cylinder, supplied and installed</li>
            <li>{ic('check', '')}Mains pressure valves, seismic restraints and tempering valve</li>
            <li>{ic('check', '')}Removal of the old cylinder</li>
          </ul>
          <p class="fine">Installed to existing plumbing in the same location. Outdoor options available. Electrical work not included. Terms and conditions apply.</p>
          <a class="btn btn-primary" href="{mail_deal}" target="_blank" rel="noopener">{ic('mail')}Ask about this deal</a>
        </div>
      </article>
    </div>
  </div>
</section>

<!-- ABOUT -->
<section id="about" class="band-light">
  <div class="wrap split">
    <div class="split-img wipe-up">
      {pic("greeting-customer", "Northland Plumbing plumber greeting a customer at the door", "(max-width:900px) 100vw, 50vw")}
      <div class="corner-tag">32+ years<br>combined</div>
      <div class="inset">{pic("team-in-van", "The team in a Northland Plumbing van", "(max-width:900px) 40vw, 22vw")}</div>
    </div>
    <div>
      <span class="eyebrow reveal">About us</span>
      <h2 class="reveal">Two local firms. One straight-talking crew.</h2>
      <p class="muted reveal">Northland Plumbing, Gas &amp; Drainage brought two Whangārei plumbing and gas fitting companies together. Hamish Smith and Duncan Jones merged Titan Gas &amp; Plumbing and Hooked Up Plumbing &amp; Gas, giving you over 32 years of combined plumbing, gas fitting and drainage experience.</p>
      <p class="muted reveal">Our qualified and trade-certified plumbers, gasfitters and drainlayers are based in Whangārei and work throughout Northland, on everything from new homes and commercial builds to a dripping tap.</p>
      <ul class="checklist reveal">
        <li>{ic('check')}<span>Talk to us at the planning stage<small>Wastewater reports and careful planning before you go to council usually save money.</small></span></li>
        <li>{ic('check')}<span>Start to finish, minimal downtime<small>Digging, drainlaying, plumbing and gas, all one team.</small></span></li>
        <li>{ic('check')}<span>No hidden costs<small>Clear communication and honest, down to earth advice.</small></span></li>
      </ul>
    </div>
  </div>
</section>

<!-- STATS -->
<section class="parallax" aria-label="By the numbers">
  <div class="bg" id="parallaxBg">{pic("toolbox-van", "", "100vw")}</div>
  <div class="wrap">
    <div class="stats">
      <div class="stat reveal"><div class="n"><span data-count="32">32</span><em>+</em></div><p>Years combined experience</p></div>
      <div class="stat reveal"><div class="n"><span data-count="10000">10,000</span><em>L</em></div><p>Fresh water per tanker load</p></div>
      <div class="stat reveal"><div class="n"><span data-count="4.5" data-dec="1">4.5</span><em>★</em></div><p>Google rating, 77 reviews</p></div>
      <div class="stat reveal"><div class="n"><span data-count="10">10</span></div><p>Services under one roof</p></div>
    </div>
  </div>
</section>

<!-- WATER DELIVERY -->
<section id="water" class="water">
  <div class="wrap">
    <div class="water-top">
      <div>
        <span class="eyebrow reveal" style="color:var(--accent-deep)">Water delivery</span>
        <h2 class="reveal">Tank running dry? 0800 WANT H2O.</h2>
        <p class="muted reveal">Our tankers carry up to 10,000 litres of fresh, potable water straight to your tank or pool, across the Whangārei and Dargaville districts. Book a time that suits you, with fair pricing based on your zone.</p>
        <ul class="pill-list reveal">
          <li>{ic('shield', '')}Taumata Arowai registered carrier</li>
          <li>{ic('drop', '')}Up to 10,000 L per load</li>
          <li>{ic('truck', '')}Tanks, pools and storage</li>
        </ul>
        <div class="big-call reveal">
          <a class="btn btn-dark" href="{H2O_TEL}">{ic('phone')}Call {H2O_TXT}</a>
          <a class="btn btn-line" href="services/water-delivery.html">Delivery zones {ic('arrow')}</a>
        </div>
      </div>
      <div class="water-photos">
        <figure class="wipe-up">{pic("water-truck-pool", "Water tanker filling a swimming pool, from above", "(max-width:960px) 60vw, 33vw")}</figure>
        <figure class="wipe-up">{pic("water-truck-filling", "Water tanker being filled at the pump station", "(max-width:960px) 40vw, 22vw")}</figure>
        <figure class="wipe-up">{pic("water-truck-shed", "The 0800 WANT H2O water tanker", "(max-width:960px) 40vw, 22vw")}</figure>
      </div>
    </div>
  </div>
</section>

<!-- BRANDS -->
<section class="brands" aria-label="Brands we install and partner with">
  <p>Brands we install, service and partner with</p>
  <div class="marquee">{brand_ul(False)}{brand_ul(True)}</div>
</section>

<!-- RECENT JOBS -->
<section id="jobs" class="band-dark">
  <div class="wrap">
    <div class="section-head">
      <div><span class="eyebrow reveal">On the job</span><h2 class="reveal">From the trench to the tap</h2></div>
      <p class="muted reveal">A look at recent work around Northland. Tap a photo to see it bigger.</p>
    </div>
    <div class="masonry">
{gallery}
    </div>
    <div class="center reveal"><a class="btn btn-ghost" href="{FB}" target="_blank" rel="noopener">{ic('fb', '')}More on Facebook</a></div>
  </div>
</section>

<!-- TEAM -->
<section id="team" class="band-light">
  <div class="wrap">
    <div class="section-head">
      <div><span class="eyebrow reveal">The crew</span><h2 class="reveal">Locals who answer the phone</h2></div>
      <p class="muted reveal">A full team of plumbers, gasfitters, drainlayers and operators, with a fleet of vans, diggers and tankers based on Lower Dent Street.</p>
    </div>
    <figure class="team-photo wipe-up">{pic("hero-team-aerial", "The whole Northland Plumbing, Gas & Drainage team with the fleet", "100vw")}<figcaption>The Northland PG team and fleet</figcaption></figure>
    <div class="team-grid">
      <div class="team-card reveal"><div class="mark">{ic('hat', '')}</div><span class="role">Co-owner</span><h3>Hamish Smith</h3><p>Founded Titan Gas &amp; Plumbing before the merger. Customers mention him by name for picking up the phone.</p></div>
      <div class="team-card reveal"><div class="mark">{ic('flame', '')}</div><span class="role">Co-owner</span><h3>Duncan Jones</h3><p>Founded Hooked Up Plumbing &amp; Gas before the merger that formed Northland PG.</p></div>
      <div class="team-card reveal"><div class="mark">{ic('wrench', '')}</div><span class="role">On the tools</span><h3>Plumbers &amp; gasfitters</h3><p>Qualified, registered and certified for residential, commercial and maintenance work.</p></div>
      <div class="team-card reveal"><div class="mark">{ic('digger', '')}</div><span class="role">Civil crew</span><h3>Drainlayers &amp; operators</h3><p>Board-certified drainlayers and qualified digger operators for drainage and earthworks.</p></div>
    </div>
    <div class="hiring reveal">
      <div><strong>We're hiring</strong><span>Experienced tradesman plumber / gasfitter. Vehicle, phone and tool account supplied.</span></div>
      <a class="btn btn-primary" href="{JOB_AD}" target="_blank" rel="noopener">View the job {ic('arrow')}</a>
    </div>
  </div>
</section>

<!-- REVIEWS -->
<section id="reviews" class="band-dark">
  <div class="wrap">
    <div class="section-head">
      <div><span class="eyebrow reveal">Reviews</span><h2 class="reveal">What Northland says</h2></div>
      <p class="muted reveal">Real reviews from our Google Business Profile.</p>
    </div>
    <div class="review-summary reveal">
      <a class="summary-card" href="{G_REVIEWS}" target="_blank" rel="noopener">{G}<span class="num">4.5</span><div>{STARS45}<small>77 reviews on Google</small></div></a>
      <a class="summary-card" href="{FB}reviews" target="_blank" rel="noopener"><svg class="fb" aria-hidden="true"><use href="#i-fb"/></svg><span class="num">92%</span><div><strong style="color:#fff">Recommended</strong><small>8 reviews on Facebook</small></div></a>
    </div>
    <div class="reviews-grid">
{chr(10).join(reviews)}
    </div>
    <div class="center reveal">
      <a class="btn btn-ghost" href="{G_REVIEWS}" target="_blank" rel="noopener">See all 77 Google reviews {ic('arrow')}</a>
    </div>
  </div>
</section>

<!-- LEAVE A REVIEW -->
<section class="review-banner" aria-label="Leave a review">
  <div class="wrap">
    <div><h2>Happy with the job? Leave us a review</h2><p>It helps other Northlanders find a plumber they can trust.</p></div>
    <a class="btn" href="{G_WRITE}" target="_blank" rel="noopener">{G}Review us on Google</a>
  </div>
</section>

<!-- FAQ -->
<section id="faq" class="band-mist">
  <div class="wrap faq-grid">
    <div class="faq-side"><span class="eyebrow reveal">FAQ</span><h2 class="reveal">Before you call</h2><p class="muted reveal">Still unsure? Ring {GAS_TXT} and ask the team.</p><a class="btn btn-dark reveal" href="{GAS_TEL}">{ic('phone')}{GAS_DIGITS}</a></div>
    <div class="faq-list reveal">
{faq_html(HOME_FAQ)}
    </div>
  </div>
</section>

{contact_section("")}
{map_section()}
</main>

<dialog class="lightbox" id="lightbox" aria-label="Photo viewer"><button type="button" aria-label="Close">&times;</button><img src="data:," alt=""><p></p></dialog>
"""
    out += footer("")
    return out

# ---------------------------------------------------------------- service page
def service_page(s):
    p = "../"
    def ppic(name, alt, sizes, **kw):
        return pic(name, alt, sizes, prefix=p, **kw)
    others = "".join(f'<a href="{o["slug"]}.html">{o["title"]}{ic("arrow", "")}</a>' for o in SERVICES if o["slug"] != s["slug"])
    lst = "".join(f"<li>{ic('check', '')}{e(x)}</li>" for x in s["list"])
    body = "".join(f'<p class="reveal">{e(x)}</p>' for x in s["body"])
    photos = "".join(ppic(n, f'{s["title"]} work by Northland Plumbing, Gas & Drainage', "(max-width:600px) 50vw, 33vw") for n in s["photos"])
    brands = ""
    if s.get("brands"):
        brands = '<div class="brand-cards">' + "".join(f'<div class="brand-card reveal"><img src="{p}img/brands/logo-{f}" alt="{e(t)} logo" loading="lazy"><h3>{e(t)}</h3><p>{e(d)}</p></div>' for f, t, d in s["brands"]) + "</div>"
    zones = ""
    if s["slug"] == "water-delivery":
        zones = f'''<div class="zones">
        <div class="zone reveal"><h3>Whangārei delivery zones</h3><img src="{p}img/map-whangarei-zones.jpg" alt="Map of water delivery zones within the Whangārei district" width="1087" height="1006" loading="lazy" data-img-role="small"></div>
        <div class="zone reveal"><h3>Dargaville delivery zones</h3><img src="{p}img/map-dargaville-zones.jpg" alt="Map of water delivery zones around Dargaville" width="1400" height="1281" loading="lazy" data-img-role="small"></div>
      </div>'''
    tel, tel_txt = (H2O_TEL, H2O_TXT) if s["slug"] == "water-delivery" else (GAS_TEL, GAS_TXT)
    mail = gmail(f'{s["title"]} enquiry', f"Hi Northland Plumbing, Gas & Drainage,\n\nI'd like a quote for {s['title'].lower()}:\n\nAddress:\n\nThanks")
    ld = {"@context": "https://schema.org", "@type": "Service", "name": s["title"], "serviceType": s["title"], "provider": {"@type": "Plumber", "name": NAME, "telephone": "+64 800 926 8427", "url": SITE_URL + "/"}, "areaServed": "Northland, New Zealand", "description": s["lead"]}
    out = head(f'{s["title"]} | {NAME}, Whangārei', s["lead"], f'services/{s["slug"]}.html', prefix=p,
               extra_ld=f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n')
    out += ribbon(p) + nav(p, None)
    out += f"""
<main id="main">
<section class="page-hero">
  {ppic(s["tile"], s["title"], "100vw", eager=True)}
  <div class="wrap">
    <ol class="crumbs hero-fade"><li><a href="{p}index.html">Home</a></li><li><a href="{p}index.html#services">Services</a></li><li>{e(s["title"])}</li></ol>
    <span class="eyebrow hero-fade">{e(s["eyebrow"])}</span>
    <h1 class="hero-fade">{e(s["h1"])}</h1>
    <p class="lead hero-fade">{e(s["lead"])}</p>
    <div class="hero-ctas hero-fade" style="display:flex;flex-wrap:wrap;gap:12px;margin-top:26px">
      <a class="btn btn-primary" href="{tel}">{ic('phone')}Call {tel_txt}</a>
      <a class="btn btn-ghost" href="{mail}" target="_blank" rel="noopener">Email us {ic('mail')}</a>
    </div>
  </div>
</section>

<section class="band-light">
  <div class="wrap svc-body">
    <div class="prose">
      <span class="eyebrow reveal">{e(s["title"])}</span>
      <h2 class="reveal">How we can help</h2>
      {body}
      <div class="svc-photos reveal">{photos}</div>
      {brands}
      {zones}
    </div>
    <aside class="svc-aside reveal">
      <h3>What's included</h3>
      <ul>{lst}</ul>
      <a class="btn btn-primary" href="{tel}">{ic('phone')}{tel_txt}</a>
      <a class="btn btn-ghost" href="{mail}" target="_blank" rel="noopener">{ic('mail')}Email the team</a>
      <a class="rating" style="margin-top:14px" href="{G_REVIEWS}" target="_blank" rel="noopener" aria-label="Rated 4.5 out of 5 from 77 Google reviews">{G}<span class="num">4.5</span><div>{STARS45}<small>77 Google reviews</small></div></a>
    </aside>
  </div>
</section>

<section class="band-mist">
  <div class="wrap faq-grid">
    <div class="faq-side"><span class="eyebrow reveal">Questions</span><h2 class="reveal">{e(s["title"])} FAQ</h2><p class="muted reveal">Anything else, just call {tel_txt}.</p></div>
    <div class="faq-list reveal">
{faq_html([(a, e(b)) for a, b in s["faq"]])}
    </div>
  </div>
</section>

<section class="band-dark">
  <div class="wrap">
    <div class="section-head"><div><span class="eyebrow reveal">More services</span><h2 class="reveal">One crew for the whole job</h2></div></div>
    <div class="other-svcs reveal">{others}</div>
  </div>
</section>

{contact_section(p)}
</main>
"""
    out += footer(p)
    # fix in-page links that should point home from sub pages
    return out

def legal(title, slug, sections):
    out = head(f"{title} | {NAME}", f"{title} for the {NAME} website.", slug)
    out += ribbon("") + nav("", sub=True, solid=True)
    body = "".join(f"<h2>{h}</h2>" + "".join(f"<p>{x}</p>" for x in ps) for h, ps in sections)
    out += f'<main id="main"><section class="legal band-light"><div class="wrap"><span class="eyebrow">{NAME}</span><h1>{title}</h1>{body}</div></section></main>\n'
    out += footer("")
    return out

PRIVACY = [
    ("What we collect", ["When you call, email or message us, we collect the details you give us, such as your name, phone number, email, the job address and what you need done."]),
    ("How we use it", ["We use your details to quote, book and complete your job, to issue invoices and compliance certificates, and to contact you about your work. We do not sell your information."]),
    ("This website", ["This site has no forms and does not set advertising cookies. The embedded Google Map and Google Fonts are provided by Google and are covered by Google's privacy policy."]),
    ("Your rights", [f"Under the Privacy Act 2020 you can ask to see or correct the personal information we hold about you. Email {EMAIL_TEXT} or call {ADMIN_TXT}."]),
]
TERMS = [
    ("About this site", [f"This website is operated by {NAME}, {ADDRESS}. Information on this site is general and may change without notice."]),
    ("Quotes and pricing", ["Quotes are provided after we understand the job. Advertised deals include GST, exclude electrical work unless stated, and are subject to terms and conditions. Water delivery prices depend on zone and access."]),
    ("Links", ["This site links to third-party sites such as Google, Facebook and product manufacturers. We are not responsible for their content."]),
    ("Contact", [f"Questions about these terms? Call {GAS_TXT} ({GAS_DIGITS}) or email {EMAIL_TEXT}."]),
]

def not_found():
    out = head(f"Page not found | {NAME}", "That page could not be found.", "404.html", prefix="/")
    out += ribbon("/") + nav("/", solid=True)
    out += f'<main id="main"><section class="legal band-light"><div class="wrap"><span class="eyebrow">Error 404</span><h1>Wrong turn</h1><p>That page has moved or never existed. Head back to the <a href="/index.html">homepage</a>, or call <a href="{GAS_TEL}">{GAS_TXT}</a>.</p></div></section></main>\n'
    out += footer("/")
    return out

def main():
    (ROOT / "services").mkdir(exist_ok=True)
    (ROOT / "index.html").write_text(home())
    for s in SERVICES:
        (ROOT / "services" / f'{s["slug"]}.html').write_text(service_page(s))
    (ROOT / "privacy.html").write_text(legal("Privacy policy", "privacy.html", PRIVACY))
    (ROOT / "terms.html").write_text(legal("Terms of use", "terms.html", TERMS))
    (ROOT / "404.html").write_text(not_found())
    urls = [""] + [f'services/{s["slug"]}.html' for s in SERVICES] + ["privacy.html", "terms.html"]
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{SITE_URL}/{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")
    (ROOT / "llms.txt").write_text(f"# {NAME}\n\n> Whangārei plumbers, gasfitters and certified drainlayers working across Northland, New Zealand.\n\n- Phone: {GAS_TXT} ({GAS_DIGITS}); water delivery {H2O_TXT} ({H2O_DIGITS}); office {ADMIN_TXT}\n- Email: {EMAIL_USER}@{EMAIL_DOMAIN}\n- Address: {ADDRESS}\n- Hours: Monday to Friday 8am to 4.30pm\n- Google rating: 4.5 from 77 reviews\n\n## Services\n" + "".join(f'- [{s["title"]}]({SITE_URL}/services/{s["slug"]}.html): {s["blurb"]}\n' for s in SERVICES))
    print("built", len(SERVICES) + 4, "pages")

if __name__ == "__main__":
    main()
