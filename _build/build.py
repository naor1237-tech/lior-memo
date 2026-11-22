# -*- coding: utf-8 -*-
"""Generates the inner landing pages + sitemap for lior-mamo.netlify.app.
Run from the site folder:  python _build/build.py
Home page (index.html) is hand-edited; this script only rewrites its shared nav/footer blocks."""
import json, os, re, html, sys

SITE = "https://lior-mamo.netlify.app"
PHONE, PHONE_INTL = "050-6737715", "+972-50-673-7715"
WA = "https://wa.me/972506737715"
UPLOAD = "2026-11-22"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

VIDEOS = {
  "showreel": ("שואוריל – ליאור ממו, חזן ופייטן", "קטעים נבחרים מעליות לתורה, ערבי פיוט ונגינה והופעה לחיילים במילואים.", "PT37S"),
  "yeled-gadol": ("״ילד גדול״ – עלייה לתורה בבית הכנסת משכן יצחק, ירושלים", "ליאור ממו שר ״ילד גדול״ בעלייה לתורה בבית הכנסת ״משכן יצחק״ בירושלים, בליווי קלידים.", "PT41S"),
  "birkat-kohanim": ("ברכת כהנים – ״ישא ה׳ פניו אליך״ בעלייה לתורה", "ליאור ממו שר ברכת כהנים – ״ישא ה׳ פניו אליך וישם לך שלום״ – בעלייה לתורה, בליווי קלידים.", "PT56S"),
  "hazan-tefillin": ("חזנות בעלייה לתורה – ליאור ממו", "תפילה חגיגית ושירה עם הקהל בעלייה לתורה.", "PT1M31S"),
  "shivchei-yerushalayim": ("״שבחי ירושלים״ – עלייה לתורה בליווי הרכב נגנים", "ליאור ממו מעלה לתורה למשפחת כהן, בליווי הרכב נגנים.", "PT55S"),
  "ya-ozel": ("״יא עוזל פלפלו״ – עוד וכינור", "עוד: ליאור ממו · כינור: דניאל זכאי.", "PT48S"),
  "zman-lisloach": ("״זה הזמן לסלוח״ – מול חומות ירושלים", "ליאור ממו מנגן עם האחים ארז מול חומות ירושלים.", "PT23S"),
  "miluim": ("שירה לחיילים במילואים", "הופעה ביחידת מילואים, בין המשימות.", "PT31S"),
  "ensemble": ("ערב מוזיקה מזרחית – עוד, כינור וכלי הקשה", "הרכב מזרחי עם ליאור ממו בעוד.", "PT25S"),
}
CARD = {  # gallery card text
  "yeled-gadol": ("״ילד גדול״", "עלייה לתורה · משכן יצחק, ירושלים", "0:41"),
  "birkat-kohanim": ("ברכת כהנים", "״ישא ה׳ פניו אליך״", "0:56"),
  "hazan-tefillin": ("חזנות בעלייה לתורה", "תפילה חגיגית ושירה עם הקהל", "1:31"),
  "shivchei-yerushalayim": ("״שבחי ירושלים״", "עלייה לתורה בליווי הרכב נגנים", "0:55"),
  "ya-ozel": ("״יא עוזל פלפלו״", "עוד וכינור", "0:48"),
  "zman-lisloach": ("״זה הזמן לסלוח״", "מול חומות ירושלים", "0:23"),
  "miluim": ("שירה לחיילים", "במילואים", "0:31"),
  "ensemble": ("ערב מוזיקה מזרחית", "עוד, כינור וכלי הקשה", "0:25"),
  "showreel": ("שואוריל", "רגעים נבחרים מהבמה", "0:37"),
}

PAGES = [
 dict(slug="bar-mitzvah", nav="בר מצווה",
  title="פייטן וחזן לבר מצווה בירושלים | עלייה לתורה עם נגנים – ליאור ממו",
  desc="מחפשים פייטן או חזן לבר מצווה? ליאור ממו – חזן, פייטן ונגן עוד: עלייה לתורה חגיגית בבית הכנסת, פיוטים ושירה בליווי נגנים. ירושלים והסביבה. 050-6737715",
  label="בר מצווה · עלייה לתורה", h1="פייטן וחזן<br><em>לבר מצווה</em>",
  lede="העלייה לתורה היא הרגע שכל המשפחה מחכה לו. ליאור ממו – חזן, פייטן ונגן עוד – הופך אותו לחגיגה: תפילה מרוממת, פיוטים ושירה בליווי נגנים, מהכניסה לבית הכנסת ועד הסעודה.",
  poster="yeled-gadol", service="פייטן וחזן לבר מצווה",
  body="""
<h2>עלייה לתורה שכל המשפחה שרה בה</h2>
<p>בר מצווה טובה נמדדת ברגעים: הרגע שהבר מצווה ניגש לספר התורה, הרגע שהקהל פורץ בשירה, והרגע שהסבא והסבתא מוחים דמעה. התפקיד של פייטן לבר מצווה הוא לייצר את הרגעים האלה – להוביל את התפילה, לבחור את הניגון הנכון בזמן הנכון ולסחוף את הקהל.</p>
<p>ליאור משלב חזנות ופיוט עם נגינה חיה, כך שהעלייה לתורה מרגישה כמו אירוע ולא רק כמו טקס. אפשר לראות את זה בסרטונים למטה – למשל ״ילד גדול״ מתוך עלייה לתורה בבית הכנסת ״משכן יצחק״ בירושלים.</p>
<h2>מה כולל השירות</h2>
<ul>
<li><b>חזנות בתפילה</b> – הובלת התפילה בנוסח שמתאים למשפחה, בקול מרומם ומרגש.</li>
<li><b>פיוטים ושירים בעלייה לתורה</b> – ליווי הבר מצווה מהרגע שהוא עולה ועד הסיום, עם שירה שהקהל מצטרף אליה.</li>
<li><b>ליווי נגנים</b> – קלידים, עוד, כינור וכלי הקשה, לפי גודל האירוע והאופי שלו.</li>
<li><b>שירה בסעודה ובקבלת הפנים</b> – פיוטים, שירי קודש וזמר שממשיכים את השמחה אחרי בית הכנסת.</li>
<li><b>הכנה לבר מצווה</b> – לימוד קריאה בתורה, טעמי המקרא וההפטרה. <a href="/hachana-bar-mitzvah/">לפרטים על ההכנה לבר מצווה</a>.</li>
</ul>
<h2>חזן, פייטן או זמר – מה ההבדל?</h2>
<p><b>חזן</b> מוביל את התפילה ואת הקריאה בבית הכנסת. <b>פייטן</b> מתמחה בפיוטים ובשירי קודש מהמסורת, ומביא אותם לרגעי השמחה. <b>זמר לבר מצווה</b> בדרך כלל מופיע בעיקר באולם. היתרון בליאור הוא שהוא עושה את שלושתם – חזן ופייטן בבית הכנסת, ונגן עוד וזמר בסעודה – כך שיש לכם איש מקצוע אחד שמלווה את כל היום.</p>
<h2>איך זה עובד</h2>
<h3>1. שיחת היכרות</h3>
<p>מספרים על התאריך, בית הכנסת או המקום, והמסורת של המשפחה. לא יודעים מה הפרשה? <a href="/parasha/">מחשבון פרשת בר מצווה</a> יגיד לכם תוך שנייה.</p>
<h3>2. בחירת הרפרטואר</h3>
<p>בוחרים יחד את הפיוטים והשירים לכל רגע – הכניסה, העלייה לתורה, סיום הקריאה ושירה לבר מצווה – ומחליטים על הרכב הנגנים.</p>
<h3>3. יום השמחה</h3>
<p>ליאור מגיע מוכן ומתואם, ואתם פשוט נהנים מהרגע.</p>
""",
  vids=["yeled-gadol","birkat-kohanim","shivchei-yerushalayim"],
  faq=[
   ("כמה עולה פייטן לבר מצווה?", "המחיר תלוי בסוג האירוע (עלייה לתורה בלבד או גם סעודה), במשך הזמן, במיקום ובהרכב הנגנים. שלחו את הפרטים בוואטסאפ ותקבלו הצעת מחיר מותאמת – בלי התחייבות."),
   ("האם ליאור מגיע לבית הכנסת שלנו?", "כן – העליות לתורה מתקיימות בבית הכנסת שתבחרו. ליאור פועל בירושלים והסביבה; לאירועים במקומות אחרים צרו קשר לבדיקת זמינות."),
   ("אפשר להגיע עם נגנים?", "כן. אפשר להזמין ליווי של קלידים, עוד, כינור וכלי הקשה – מנגן יחיד ועד הרכב מלא, לפי האופי והתקציב."),
   ("כמה זמן מראש כדאי להזמין?", "תאריכים של בר מצווה – בעיקר בימי שני, חמישי וראש חודש – מתמלאים מהר. מומלץ לפנות ברגע שהתאריך ידוע."),
   ("האם ליאור גם מכין את הבר מצווה?", "כן. ליאור מלמד קריאה בתורה, טעמי המקרא וההפטרה. ראו את עמוד <a href=\"/hachana-bar-mitzvah/\">הכנה לבר מצווה</a>."),
   ("איך יודעים מה הפרשה של הבר מצווה?", "הפרשה נקבעת לפי התאריך העברי של יום הולדת 13. אפשר לבדוק אותה במחשבון שלנו: <a href=\"/parasha/\">מה הפרשה שלי לבר מצווה</a>."),
  ]),
 dict(slug="shabbat-chatan", nav="שבת חתן",
  title="פייטן לשבת חתן | חזן ופיוטים לשבת חתן – ליאור ממו",
  desc="פייטן וחזן לשבת חתן: חזנות מרוממת בתפילה, פיוטים ושירים בסעודות ועוד בליווי. ליאור ממו – ירושלים והסביבה. לבדיקת תאריך: 050-6737715",
  label="שבת חתן · שבת עלייה", h1="פייטן וחזן<br><em>לשבת חתן</em>",
  lede="שבת חתן היא שבת אחת בחיים. ליאור ממו מביא אליה חזנות מרוממת בתפילה, פיוטים ושירים בסעודות ונגינה בעוד – כדי שהחתן, המשפחה והאורחים ייזכרו בה שנים.",
  poster="hazan-tefillin", service="פייטן וחזן לשבת חתן",
  body="""
<h2>שבת שכולה שירה</h2>
<p>בשבת שלפני החתונה עולה החתן לתורה, והמשפחה והחברים מתכנסים סביבו לתפילה ולסעודות. פייטן לשבת חתן הוא מי שנותן לשבת הזאת את הקצב והנשמה: מוביל את התפילה, פותח את הסעודה בפיוט ומרים את השירה בשולחן.</p>
<p>ליאור הוא חזן ופייטן שמכיר את הרגעים האלה מקרוב – מהעלייה לתורה בבית הכנסת ועד שירת השבת בסעודה – ויודע להתאים את עצמו לקהל, לנוסח ולמסורת של המשפחה.</p>
<h2>מה ליאור מביא לשבת החתן</h2>
<ul>
<li><b>חזנות בתפילות השבת</b> – תפילה מרוממת ומרגשת שמכבדת את החתן ואת הקהל.</li>
<li><b>העלייה לתורה של החתן</b> – פיוטים ושירים לכבוד החתן ברגע שהוא עולה לתורה.</li>
<li><b>פיוטים ושירים בסעודות</b> – זמירות שבת, פיוטים ושירי קודש שכל השולחן מצטרף אליהם.</li>
<li><b>שבע ברכות</b> – גם אחרי החתונה: פיוטים וזמר לערבי שבע ברכות.</li>
<li><b>נגינה בעוד</b> – בערבים שלפני השבת ואחריה, לקבלת פנים או לערב שירה.</li>
</ul>
<h2>מותאם למסורת שלכם</h2>
<p>כל משפחה והניגונים שלה. לפני השבת יושבים יחד ובוחרים את הנוסח, את הפיוטים ואת השירים שחשובים לכם – כדי שבשבת עצמה הכול יזרום בטבעיות.</p>
<p>מחפשים גם פייטן לבר מצווה במשפחה? <a href="/bar-mitzvah/">פייטן וחזן לבר מצווה</a>.</p>
""",
  vids=["hazan-tefillin","zman-lisloach","ya-ozel"],
  faq=[
   ("מה עושה פייטן בשבת חתן?", "הפייטן מוביל את התפילה, מלווה את העלייה לתורה של החתן בפיוטים ושירים, ומוביל את השירה בסעודות השבת."),
   ("כמה עולה פייטן לשבת חתן?", "המחיר תלוי במשך ההשתתפות (תפילה, סעודות או שבת מלאה), במיקום ובצרכים הלוגיסטיים. שלחו פרטים ותקבלו הצעת מחיר מותאמת."),
   ("איך מתאמים שבת שלמה?", "שבת דורשת תיאום מראש של מקום ולוגיסטיקה. מספרים לליאור על המקום והתוכנית, ומתאמים את כל הפרטים מבעוד מועד."),
   ("אפשר להזמין גם לשבע ברכות?", "כן – ליאור מגיע לערבי שבע ברכות עם פיוטים, זמר ונגינה בעוד."),
   ("באיזה אזור ליאור פועל?", "ירושלים והסביבה. לאירועים באזורים אחרים צרו קשר לבדיקת זמינות."),
  ]),
 dict(slug="hachana-bar-mitzvah", nav="הכנה לבר מצווה",
  title="הכנה לבר מצווה | לימוד הפרשה וההפטרה בטעמים – ליאור ממו",
  desc="הכנה לבר מצווה עם חזן ובעל קורא: לימוד קריאה בתורה, טעמי המקרא, הפטרה וברכות – בסבלנות ובגובה העיניים. ליאור ממו, ירושלים. 050-6737715",
  label="הכנה לבר מצווה · קריאה בתורה", h1="הכנה<br><em>לבר מצווה</em>",
  lede="ליווי אישי של הבר מצווה: לימוד הפרשה, המפטיר וההפטרה בטעמים לפי מסורת המשפחה – הכנה מדויקת עם חזן ובעל קורא, ועד העלייה לתורה, גם בליווי נגנים.",
  poster="hazan-tefillin", service="הכנה לבר מצווה – לימוד קריאה בתורה",
  body="""
<h2>להגיע לעלייה לתורה בביטחון</h2>
<p>הרגע שבו הבר מצווה קורא בתורה מול כל הקהל מתחיל חודשים קודם, בלימוד. הכנה טובה לבר מצווה לא נגמרת בשינון: היא בונה ביטחון, מלמדת להבין את הטעמים ואת המילים, ומכינה את הנער לעמוד מול קהל ולהנות מזה.</p>
<p>ליאור הוא חזן ובעל קורא, ומלמד את הקריאה בדיוק כמו שהוא עושה אותה בבית הכנסת – עם יחס אישי, סבלנות ושפה שנערים מתחברים אליה.</p>
<h2>מה לומדים בהכנה לבר מצווה</h2>
<ul>
<li><b>קריאה בתורה</b> – קריאת הפרשה (או חלק ממנה) מתוך ספר התורה, בדגש על הגייה נכונה.</li>
<li><b>טעמי המקרא</b> – הנגינה של הקריאה, כך שהנער יבין את המבנה ולא רק יזכור בעל פה.</li>
<li><b>ההפטרה</b> – לימוד ההפטרה והברכות שלפניה ואחריה.</li>
<li><b>ברכות העלייה לתורה</b> – הברכות שהבר מצווה אומר כשהוא עולה לתורה.</li>
<li><b>עמידה מול קהל</b> – תרגול שמכין את הנער לרגע האמיתי.</li>
</ul>
<h2>לימוד בטעמים – לפי המסורת שלכם</h2>
<p>לכל קהילה הנגינה שלה. ליאור מלמד את הקריאה <b>במגוון נוסחי טעמים</b>, ובוחרים יחד את הנוסח שמתאים למסורת המשפחה ולבית הכנסת שבו תתקיים העלייה לתורה. ההכנה מדויקת: כל מילה, כל טעם וכל ברכה – עד שהבר מצווה קורא בביטחון ובהנאה.</p>
<ul>
<li><b>שלב 1 – מוצאים את הפרשה</b>: <a href="/parasha/">מחשבון הפרשה</a> מחשב פרשה, מפטיר והפטרה לפי הנוסח שלכם.</li>
<li><b>שלב 2 – לימוד מדויק</b>: קריאה, טעמים, מפטיר, הפטרה וברכות – בקצב של הנער.</li>
<li><b>שלב 3 – חזרה גנרלית</b>: תרגול מול קהל קטן, כדי שביום עצמו הכול ירגיש מוכר.</li>
<li><b>שלב 4 – היום הגדול</b>: ליאור יכול ללוות את העלייה לתורה כחזן ופייטן, גם עם נגנים.</li>
</ul>
<h2>מתי להתחיל?</h2>
<p>בדרך כלל מומלץ להתחיל את ההכנה כמה חודשים לפני הבר מצווה – משך הזמן תלוי בהיקף הקריאה ובקצב של הנער. כדאי לבדוק קודם מה הפרשה: <a href="/parasha/">מחשבון פרשת בר מצווה</a>.</p>
<h2>וביום עצמו</h2>
<p>ליאור יכול ללוות את הבר מצווה גם ביום השמחה – כחזן ופייטן בעלייה לתורה, עם שירה ונגנים. <a href="/bar-mitzvah/">פייטן וחזן לבר מצווה</a>.</p>
""",
  vids=["hazan-tefillin","yeled-gadol","shivchei-yerushalayim"],
  faq=[
   ("כמה עולה מורה לבר מצווה?", "המחיר תלוי במספר המפגשים, בהיקף הקריאה (פרשה מלאה, חלק ממנה, הפטרה) ובמיקום. צרו קשר לקבלת הצעה מותאמת."),
   ("כמה זמן לפני הבר מצווה מתחילים ללמוד?", "בדרך כלל כמה חודשים מראש. זה תלוי בהיקף הקריאה ובקצב של הנער – בשיחה הראשונה בונים תוכנית מתאימה."),
   ("איך יודעים איזו פרשה הבר מצווה קורא?", "הפרשה נקבעת לפי התאריך העברי של יום הולדת 13. השתמשו ב<a href=\"/parasha/\">מחשבון הפרשה</a> שלנו."),
   ("באיזה נוסח טעמים לומדים?", "ליאור מלמד במגוון נוסחי טעמים, ובוחרים יחד את הנוסח לפי מסורת המשפחה ובית הכנסת. אפשר לציין את הנוסח כבר במחשבון הפרשה."),
   ("איפה מתקיימים השיעורים?", "מתאמים את מקום הלימוד בשיחה – צרו קשר עם ליאור לפרטים."),
   ("האם ליאור יכול גם להיות החזן בבר מצווה?", "כן – ליאור מלווה גם את העלייה לתורה עצמה כחזן ופייטן, עם שירה ונגנים."),
  ]),
 dict(slug="nagan-oud", nav="נגן עוד",
  title="נגן עוד לאירועים וחתונות | הרכב מזרחי – ליאור ממו",
  desc="נגן עוד לאירועים: קבלת פנים, חתונות, שבע ברכות, חנוכת בית וערבי פיוט. ליאור ממו בעוד, לבד או בהרכב עם כינור וכלי הקשה. 050-6737715",
  label="עוד · הרכב מזרחי", h1="נגן עוד<br><em>לאירועים</em>",
  lede="צליל העוד הופך כל קבלת פנים לחוויה. ליאור ממו מנגן בעוד ומופיע עם נגנים – כינור, כלי הקשה וקלידים – בפיוטים, בשירי קודש ובמוזיקה מזרחית.",
  poster="ya-ozel", service="נגן עוד והרכב מזרחי לאירועים",
  body="""
<h2>עוד חי באירוע שלכם</h2>
<p>העוד הוא הלב של המוזיקה המזרחית והפיוט. נגן עוד באירוע יוצר אווירה חמה ואלגנטית – ברקע של קבלת פנים, בזמן הארוחה או בערב שירה שבו כולם מצטרפים.</p>
<p>ליאור מנגן בעוד ומופיע גם עם נגנים מוכשרים, כמו בקטע ״יא עוזל פלפלו״ עם דניאל זכאי בכינור, ובערבי מוזיקה מזרחית עם כלי הקשה.</p>
<h2>לאילו אירועים</h2>
<ul>
<li><b>חתונות וקבלת פנים</b> – מוזיקה חיה ואלגנטית לפני החופה.</li>
<li><b>שבע ברכות</b> – פיוטים וזמר עם עוד בליווי.</li>
<li><b>חנוכת בית וברית</b> – ניגונים ופיוטים לשמחות משפחתיות.</li>
<li><b>בר מצווה</b> – נגינה בסעודה אחרי העלייה לתורה. <a href="/bar-mitzvah/">פייטן לבר מצווה</a>.</li>
<li><b>ערבי פיוט ושירה</b> – ערב שלם של פיוטים ומוזיקה מזרחית.</li>
</ul>
<h2>לבד או בהרכב</h2>
<p>אפשר להזמין את ליאור כנגן עוד יחיד – לאווירה אינטימית – או בהרכב עם כינור, כלי הקשה וקלידים לאירוע גדול. בוחרים יחד את ההרכב והרפרטואר לפי אופי האירוע.</p>
""",
  vids=["ya-ozel","ensemble","zman-lisloach"],
  faq=[
   ("כמה עולה נגן עוד לאירוע?", "המחיר תלוי במשך הנגינה, בהרכב (נגן יחיד או הרכב) ובמיקום. שלחו את פרטי האירוע לקבלת הצעה."),
   ("אפשר נגן עוד לחתונה?", "כן – לקבלת פנים, לפני החופה, בזמן הארוחה או לערבי שבע ברכות."),
   ("מה ההרכב שמגיע?", "מנגן עוד יחיד ועד הרכב עם כינור, כלי הקשה וקלידים – לפי מה שמתאים לאירוע."),
   ("איזה סגנון מוזיקה?", "פיוטים, שירי קודש, מוזיקה מזרחית וזמר ישראלי. את הרפרטואר מתאימים מראש לקהל ולאירוע."),
  ]),
]

PARASHA = dict(slug="parasha", nav="מה הפרשה?",
  title="מה הפרשה שלי לבר מצווה? מחשבון פרשת בר מצווה – ליאור ממו",
  desc="מחשבון פרשת בר מצווה: הזינו תאריך לידה וגלו את התאריך העברי של הבר מצווה, את שבת העלייה לתורה ואת הפרשה וההפטרה. חינם, תוך שנייה.",
)

# ---------------- partials ----------------
def sprite():
    s = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
    return re.search(r'<svg width="0" height="0".*?</svg>', s, re.S).group(0)

NAV_ITEMS = [("/#services","שירותים"),("/bar-mitzvah/","בר מצווה"),("/shabbat-chatan/","שבת חתן"),("/parasha/","מה הפרשה?")]
def nav(active=""):
    links = "\n      ".join(f'<a href="{h}"{" aria-current=\"page\"" if h.strip("/")==active else ""}>{t}</a>' for h,t in NAV_ITEMS)
    return f'''<header class="nav" id="nav">
  <div class="wrap">
    <nav class="nav-links" aria-label="ניווט ראשי">
      {links}
    </nav>
    <a href="/" class="logo" aria-label="ליאור ממו – דף הבית">ליאור ממו<small>חזן · פייטן · נגן</small></a>
    <div class="nav-cta">
      <a class="btn btn-line" href="/#contact">הזמנת אירוע</a>
      <a class="icon-btn" href="{WA}?text=%D7%A9%D7%9C%D7%95%D7%9D%20%D7%9C%D7%99%D7%90%D7%95%D7%A8%2C%20%D7%94%D7%92%D7%A2%D7%AA%D7%99%20%D7%9E%D7%94%D7%90%D7%AA%D7%A8" target="_blank" rel="noopener" aria-label="וואטסאפ"><svg><use href="#i-wa"/></svg></a>
      <button type="button" class="menu-btn" id="menuBtn" aria-label="פתיחת תפריט" aria-expanded="false" aria-controls="mnav"><i></i><i></i><i></i></button>
    </div>
  </div>
</header>
<nav class="mnav" id="mnav" aria-label="תפריט" hidden>
  <a href="/">דף הבית</a>
  <a href="/hachana-bar-mitzvah/">ליווי והכנה לבר מצווה</a>
  <a href="/parasha/">מה הפרשה של הבר מצווה?</a>
  <a href="/bar-mitzvah/">עלייה לתורה עם נגנים</a>
  <a href="/shabbat-chatan/">שבת חתן ושבע ברכות</a>
  <a href="/nagan-oud/">נגן עוד – נסו לנגן</a>
  <a href="/#gallery">סרטונים מהבמה</a>
  <a href="/#contact">הזמנת אירוע</a>
  <div class="mnav-cta"><a class="btn btn-solid" href="tel:+972506737715"><svg><use href="#i-phone"/></svg>050-6737715</a><a class="btn btn-wa" href="{WA}" target="_blank" rel="noopener"><svg><use href="#i-wa"/></svg>וואטסאפ</a></div>
</nav>'''

def footer():
    links = "".join(f'<a href="/{p["slug"]}/">{p["nav"] if p["slug"]!="parasha" else "מחשבון פרשה"}</a>' for p in PAGES+[PARASHA])
    return f'''<footer>
  <div class="wrap">
    <div class="foot">
      <a href="/" class="logo">ליאור ממו<small>חזן · פייטן · נגן</small></a>
      <nav class="foot-links" aria-label="קישורים">{links}</nav>
      <div class="foot-links"><a href="tel:{PHONE_INTL.replace('-','')}" dir="ltr">{PHONE}</a><a href="{WA}" target="_blank" rel="noopener">וואטסאפ</a></div>
    </div>
    <nav class="legal-links" aria-label="מידע משפטי"><a href="/negishut/">הצהרת נגישות</a><a href="/privacy/">מדיניות פרטיות</a><a href="/terms/">תנאי שימוש וזכויות יוצרים</a></nav>
    <div class="gift">
      <span>© <span id="yr">2026</span> ליאור ממו · חזן, פייטן ונגן עוד · ירושלים</span>
      <span>האתר נבנה במתנה, בהוקרה לאנשי המילואים, ע"י <a href="https://solutions.hilel.link/?utm_source=lior-mamo&utm_medium=footer&utm_campaign=gift-site" target="_blank" rel="noopener">הלל פתרונות</a></span>
    </div>
  </div>
</footer>'''

TAIL = f'''<a class="fab" href="{WA}?text=%D7%A9%D7%9C%D7%95%D7%9D%20%D7%9C%D7%99%D7%90%D7%95%D7%A8%2C%20%D7%94%D7%92%D7%A2%D7%AA%D7%99%20%D7%9E%D7%94%D7%90%D7%AA%D7%A8" target="_blank" rel="noopener" aria-label="שליחת הודעת וואטסאפ לליאור"><svg><use href="#i-wa"/></svg></a>

<dialog class="lb" id="lb" aria-label="נגן וידאו">
  <div class="lb-in">
    <video id="lbVid" controls playsinline preload="none"></video>
    <div class="lb-cap"><h3 id="lbT"></h3><p id="lbS"></p></div>
  </div>
  <button class="lb-btn lb-x" id="lbX" aria-label="סגירה"><svg><use href="#i-x"/></svg></button>
  <button class="lb-btn lb-p" id="lbP" aria-label="הסרטון הקודם"><svg><use href="#i-r"/></svg></button>
  <button class="lb-btn lb-n" id="lbN" aria-label="הסרטון הבא"><svg><use href="#i-l"/></svg></button>
</dialog>'''

def strip_tags(s): return re.sub(r"<[^>]+>", "", s)

BUSINESS_ID = SITE + "/#business"
def video_ld(vid):
    n, d, dur = VIDEOS[vid]
    return {"@type":"VideoObject","name":n,"description":d,"thumbnailUrl":f"{SITE}/media/{vid}.jpg",
            "contentUrl":f"{SITE}/v/{vid}.mp4","uploadDate":UPLOAD,"duration":dur,"inLanguage":"he"}

def head(title, desc, path, ld, image="og.jpg"):
    url = SITE + path
    return f'''<!doctype html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{html.escape(desc, quote=True)}">
<meta name="theme-color" content="#0b0a09">
<meta name="robots" content="index,follow,max-image-preview:large,max-video-preview:-1">
<link rel="canonical" href="{url}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="website">
<meta property="og:locale" content="he_IL">
<meta property="og:site_name" content="ליאור ממו – חזן ופייטן">
<meta property="og:title" content="{html.escape(title, quote=True)}">
<meta property="og:description" content="{html.escape(desc, quote=True)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/media/{image}">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Suez+One&family=Frank+Ruhl+Libre:wght@400;500;700&family=Assistant:wght@300;400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/site.css">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
'''

def vcard(v):
    t, s, d = CARD[v]
    return (f'<button class="item rv" data-open="{v}" aria-label="צפייה: {strip_tags(t).strip("״")}">'
            f'<span class="media"><img src="/media/{v}.jpg?v=4" alt="{html.escape(VIDEOS[v][0], quote=True)}" loading="lazy"><span class="ring"><svg><use href="#i-play"/></svg></span></span>'
            f'<span class="meta"><span><h3>{t}</h3><span class="sub">{s}</span></span><span class="dur">{d}</span></span></button>')

def faq_html(faq):
    return '<div class="faq">' + "".join(f'<details class="rv"><summary>{q}</summary><div class="ans"><p>{a}</p></div></details>' for q,a in faq) + '</div>'

def faq_ld(faq):
    return {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":strip_tags(a)}} for q,a in faq]}

def crumbs_ld(name, path):
    return {"@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"ליאור ממו","item":SITE+"/"},
        {"@type":"ListItem","position":2,"name":name,"item":SITE+path}]}

def related(current):
    items = []
    for p in PAGES+[PARASHA]:
        if p["slug"] == current: continue
        sub = {"bar-mitzvah":"עלייה לתורה עם נגנים","shabbat-chatan":"חזנות ופיוטים","hachana-bar-mitzvah":"קריאה בתורה והפטרה","nagan-oud":"עוד והרכב מזרחי","parasha":"מחשבון חינמי"}[p["slug"]]
        items.append(f'<a class="rel rv" href="/{p["slug"]}/"><small>עוד באתר</small><b>{p["nav"] if p["slug"]!="parasha" else "מה הפרשה שלי?"}</b><span>{sub}</span></a>')
    return '<div class="related">' + "".join(items) + '</div>'

def aside():
    return f'''<aside class="aside rv">
      <h3>בודקים תאריך?</h3>
      <p>שלחו הודעה עם התאריך והמקום – ליאור יחזור אליכם.</p>
      <a class="btn btn-solid" href="{WA}?text={json.dumps('')[1:-1]}" target="_blank" rel="noopener" data-wa><svg><use href="#i-wa"/></svg>וואטסאפ</a>
      <a class="btn btn-line" href="tel:+972506737715"><svg><use href="#i-phone"/></svg>חיוג</a>
      <a class="ph-num" href="tel:+972506737715">{PHONE}</a>
    </aside>'''

def cta():
    return f'''<section class="cta-band">
  <div class="wrap rv">
    <div class="orn"><svg><use href="#i-dia"/></svg></div>
    <h2>נשמח להיות<br><em>חלק מהשמחה.</em></h2>
    <p class="lede" style="margin:0 auto">ספרו לליאור על האירוע – ותקבלו מענה אישי.</p>
    <div class="row"><a class="btn btn-solid" href="{WA}" target="_blank" rel="noopener"><svg><use href="#i-wa"/></svg>שליחת הודעה</a><a class="btn btn-line" href="/#contact">טופס הזמנה</a><a class="btn btn-line" href="tel:+972506737715"><svg><use href="#i-phone"/></svg>{PHONE}</a></div>
  </div>
</section>'''

def page(p):
    path = f'/{p["slug"]}/'
    ld = {"@context":"https://schema.org","@graph":[
        {"@type":"Service","name":p["service"],"serviceType":p["service"],"description":p["desc"],
         "provider":{"@id":BUSINESS_ID},"areaServed":{"@type":"City","name":"ירושלים"},"url":SITE+path},
        crumbs_ld(p["nav"], path), faq_ld(p["faq"])] + [video_ld(v) for v in p["vids"]]}
    wa_text = "שלום ליאור, הגעתי מהאתר (עמוד " + p["nav"] + ")"
    body = head(p["title"], p["desc"], path, ld, image=f'{p["poster"]}.jpg') + sprite() + "\n\n" + nav(p["slug"]) + f'''

<main id="top">
<section class="page-hero">
  <div class="hero-bg" aria-hidden="true"><img src="/media/{p["poster"]}.jpg" alt=""></div>
  <div class="wrap ph-grid">
    <div class="rv">
      <ol class="crumbs" aria-label="פירורי לחם"><li><a href="/">ליאור ממו</a></li><li aria-current="page">{p["nav"]}</li></ol>
      <span class="label">{p["label"]}</span>
      <h1>{p["h1"]}</h1>
      <p class="lede">{p["lede"]}</p>
      <div class="hero-ctas">
        <a class="btn btn-solid" href="{WA}?text={urlq(wa_text)}" target="_blank" rel="noopener"><svg><use href="#i-wa"/></svg>לבדיקת תאריך</a>
        <a class="btn btn-line" href="tel:+972506737715"><svg><use href="#i-phone"/></svg>{PHONE}</a>
      </div>
    </div>
    <div class="reel-frame rv">
      <span class="corner c1"></span><span class="corner c2"></span>
      <div class="shell"><img src="/media/{p["poster"]}.jpg" alt="{html.escape(VIDEOS[p["poster"]][0], quote=True)}"></div>
      <button class="reel-play" data-open="{p["poster"]}" aria-label="צפייה בסרטון">
        <span class="ring"><svg><use href="#i-play"/></svg></span>
        <span><small>VIDEO<span class="bars"><i></i><i></i><i></i><i></i><i></i></span></small><b>{CARD[p["poster"]][0]}</b></span>
      </button>
    </div>
  </div>
</section>

{OUD() if p["slug"]=="nagan-oud" else ""}
<section class="sec">
  <div class="wrap content">
    <article class="prose rv">
{p["body"].strip()}
      <h2>מהאירועים</h2>
      <div class="vids">{"".join(vcard(v) for v in p["vids"])}</div>
    </article>
    {aside()}
  </div>
</section>

<section class="sec" style="padding-top:0">
  <div class="wrap">
    <div class="sec-head"><div class="rv"><span class="label">שאלות נפוצות</span><h2 class="h2">כל מה ששואלים<br><em>לפני שמזמינים.</em></h2></div></div>
    {faq_html(p["faq"])}
  </div>
</section>

<section class="sec" style="padding-top:0">
  <div class="wrap">{related(p["slug"])}</div>
</section>

{cta()}
</main>

{footer()}

{TAIL}

<script src="/js/site.js" defer></script>
{'<script src="/js/oud.js" defer></script>' if p["slug"]=="nagan-oud" else ""}
</body>
</html>
'''
    out = os.path.join(ROOT, p["slug"]); os.makedirs(out, exist_ok=True)
    open(os.path.join(out, "index.html"), "w", encoding="utf-8").write(body)

def urlq(s):
    import urllib.parse; return urllib.parse.quote(s)

PARASHA_FAQ = [
  ("איך יודעים מה הפרשה לבר מצווה?", "לוקחים את התאריך העברי של יום הלידה, מוסיפים 13 שנים עבריות, ובודקים איזו פרשה נקראת בשבת שחלה ביום ההולדת העברי או מיד אחריו. המחשבון בעמוד הזה עושה את כל החישוב בשבילכם."),
  ("למה חשוב לסמן אם הלידה הייתה אחרי השקיעה?", "היום העברי מתחיל בשקיעה. תינוק שנולד בערב, אחרי השקיעה, נולד בעצם ביום העברי הבא – ולכן גם תאריך הבר מצווה ואולי הפרשה משתנים."),
  ("למה יש הבדל בין ישראל לחוץ לארץ?", "בחלק מהשנים סדר הפרשות בישראל ובחוץ לארץ שונה לכמה שבועות (בגלל יום טוב שני של גלויות). לכן חשוב לבחור איפה תתקיים הבר מצווה."),
  ("מה קורה אם נולדתי באדר בשנה מעוברת?", "בשנה מעוברת יש שני חודשי אדר. נער שנולד באדר בשנה רגילה וחוגג בשנה מעוברת – לרוב חוגג באדר ב'. נער שנולד באדר א' או אדר ב' וחוגג בשנה רגילה – חוגג באדר. במקרים כאלה כדאי לאמת עם רב הקהילה."),
  ("האם המחשבון מדויק?", "המחשבון מבוסס על לוח השנה העברי של Hebcal. הוא מדויק ברוב המקרים, אבל במקרים מיוחדים (אדר בשנה מעוברת, 30 בחשוון או בכסלו, או שבת שחלה ביום טוב) מומלץ לאמת עם רב או חזן."),
]

def parasha_page():
    p = PARASHA; path = "/parasha/"
    ld = {"@context":"https://schema.org","@graph":[
        {"@type":"WebApplication","name":"מחשבון פרשת בר מצווה","url":SITE+path,"applicationCategory":"UtilitiesApplication","operatingSystem":"Any","inLanguage":"he",
         "offers":{"@type":"Offer","price":"0","priceCurrency":"ILS"},"provider":{"@id":BUSINESS_ID}},
        crumbs_ld("מחשבון פרשת בר מצווה", path), faq_ld(PARASHA_FAQ)]}
    body = head(p["title"], p["desc"], path, ld) + sprite() + "\n\n" + nav("parasha") + f'''

<main id="top">
<section class="page-hero">
  <div class="hero-bg" aria-hidden="true"><img src="/media/hero.jpg" alt=""></div>
  <div class="wrap" style="position:relative;z-index:1">
    <div class="rv" style="max-width:860px">
      <ol class="crumbs" aria-label="פירורי לחם"><li><a href="/">ליאור ממו</a></li><li aria-current="page">מחשבון פרשת בר מצווה</li></ol>
      <span class="label">כלי חינמי</span>
      <h1>מה הפרשה שלי<br><em>לבר מצווה?</em></h1>
      <p class="lede">הזינו את תאריך הלידה ואת נוסח הטעמים של המשפחה – וקבלו את התאריך העברי של הבר מצווה, שבת העלייה לתורה, הפרשה, המפטיר וההפטרה לפי הנוסח שלכם.</p>
    </div>
  </div>
</section>

<section class="sec" style="padding-top:80px">
  <div class="wrap content">
    <div>
      <form class="calc form rv" id="calc" novalidate>
        <h3 style="font-family:var(--display);font-weight:400;font-size:32px;margin:0 0 26px;color:var(--ivory)">תאריך הלידה של הבר מצווה</h3>
        <div class="fgrid">
          <div class="f"><label for="cDay">יום</label><input id="cDay" type="number" min="1" max="31" inputmode="numeric" placeholder="15" required></div>
          <div class="f"><label for="cMonth">חודש</label><select id="cMonth">{"".join(f'<option value="{i}">{m}</option>' for i,m in enumerate(["ינואר","פברואר","מרץ","אפריל","מאי","יוני","יולי","אוגוסט","ספטמבר","אוקטובר","נובמבר","דצמבר"],1))}</select></div>
          <div class="f"><label for="cYear">שנה</label><input id="cYear" type="number" min="1990" max="2030" inputmode="numeric" placeholder="2014" required></div>
        </div>
        <div class="f" style="margin-top:22px"><label for="cNusach">נוסח הטעמים של המשפחה</label><select id="cNusach"><option>ספרדי־ירושלמי</option><option>מרוקאי</option><option>עיראקי / בבלי</option><option>תימני</option><option>אשכנזי</option><option>עוד לא בטוחים</option></select></div>
        <label class="chk"><input type="checkbox" id="cSunset"> הלידה הייתה אחרי השקיעה</label>
        <label class="chk"><input type="checkbox" id="cDiaspora"> הבר מצווה תתקיים בחוץ לארץ</label>
        <button class="btn btn-solid" type="submit">חישוב הפרשה</button>
        <div class="result" id="res" aria-live="polite"></div>
      </form>

      <article class="prose rv" style="margin-top:90px">
        <h2>איך מחשבים את הפרשה של הבר מצווה?</h2>
        <p>נער מגיע לגיל מצוות ביום הולדתו ה-13 לפי <b>הלוח העברי</b> – לא לפי התאריך הלועזי. לכן החישוב מתחיל בתאריך העברי של הלידה:</p>
        <ul>
          <li><b>שלב 1</b> – ממירים את תאריך הלידה הלועזי לתאריך עברי (ואם הלידה הייתה אחרי השקיעה – ליום העברי הבא).</li>
          <li><b>שלב 2</b> – מוסיפים 13 שנים עבריות ומקבלים את תאריך הבר מצווה העברי.</li>
          <li><b>שלב 3</b> – מוצאים את השבת שחלה ביום הזה או מיד אחריו – זו שבת העלייה לתורה.</li>
          <li><b>שלב 4</b> – בודקים איזו פרשה והפטרה נקראות באותה שבת, בישראל או בחוץ לארץ.</li>
        </ul>
        <p class="upd" style="font-size:14px;color:var(--muted)">נתוני הלוח העברי: <a href="https://www.hebcal.com" target="_blank" rel="noopener">Hebcal.com</a> (רישיון CC BY 4.0).</p>
        <p>הרבה משפחות עורכות את העלייה לתורה גם ביום שני או חמישי שאחרי יום ההולדת – גם אז קוראים בתורה (מתחילת הפרשה של השבת הקרובה).</p>
        <h2>ובאיזו פרשה נולדתם?</h2>
        <p>פרשת הבר מצווה נקבעת לפי יום הולדת 13 – אבל יש גם את <b>פרשת הלידה</b>: הפרשה של השבוע שבו נולדתם. אפשר לגלות אותה ב<a href="https://hilel.link/parasha?utm_source=lior-mamo&amp;utm_medium=referral&amp;utm_campaign=parasha-crosslink" target="_blank" rel="noopener">מחשבון פרשת הלידה של שירה הלל</a>.</p>
        <h2>ואחרי שיודעים את הפרשה?</h2>
        <p>זה הזמן להתחיל ללמוד. ליאור ממו, חזן ובעל קורא, מלמד קריאה בתורה, טעמים והפטרה – <a href="/hachana-bar-mitzvah/">הכנה לבר מצווה</a> – ומלווה גם את העלייה לתורה עצמה עם פיוטים ונגנים: <a href="/bar-mitzvah/">פייטן וחזן לבר מצווה</a>.</p>
      </article>
    </div>
    {aside()}
  </div>
</section>

<section class="sec" style="padding-top:0">
  <div class="wrap">
    <div class="sec-head"><div class="rv"><span class="label">שאלות נפוצות</span><h2 class="h2">פרשת בר מצווה<br><em>שאלות ותשובות.</em></h2></div></div>
    {faq_html(PARASHA_FAQ)}
  </div>
</section>

<section class="sec" style="padding-top:0">
  <div class="wrap">{related("parasha")}</div>
</section>

{cta()}
</main>

{footer()}

{TAIL}

<script src="/js/site.js" defer></script>
<script src="/js/parasha.js" defer></script>
</body>
</html>
'''
    out = os.path.join(ROOT, "parasha"); os.makedirs(out, exist_ok=True)
    open(os.path.join(out, "index.html"), "w", encoding="utf-8").write(body)

def OUD():
    return open(os.path.join(ROOT, "_build", "oud_section.html"), encoding="utf-8").read()

def patch_home():
    f = os.path.join(ROOT, "index.html"); s = open(f, encoding="utf-8").read()
    s = re.sub(r'<section class="sec oud-sec" id="oud">.*?</section>\n', '', s, flags=re.S)
    s = s.replace('<section class="sec" id="gallery">', OUD() + '\n<section class="sec" id="gallery">', 1)
    if '/js/oud.js' not in s:
        s = s.replace('<script src="/js/site.js" defer></script>', '<script src="/js/site.js" defer></script>\n<script src="/js/oud.js" defer></script>', 1)
    s = re.sub(r'<header class="nav" id="nav">.*?</header>', lambda m: nav(""), s, count=1, flags=re.S)
    s = re.sub(r'<footer>.*?</footer>', lambda m: footer(), s, count=1, flags=re.S)
    open(f, "w", encoding="utf-8").write(s)

def sitemap():
    urls = [("/", "1.0", ["showreel","yeled-gadol","birkat-kohanim","hazan-tefillin","shivchei-yerushalayim","ya-ozel","zman-lisloach","miluim","ensemble"])]
    urls += [(f'/{p["slug"]}/', "0.9", p["vids"]) for p in PAGES] + [("/parasha/", "0.8", [])]
    x = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">']
    for path, pr, vids in urls:
        x.append(f"  <url><loc>{SITE}{path}</loc><lastmod>{UPLOAD}</lastmod><priority>{pr}</priority>")
        for v in vids:
            n, d, dur = VIDEOS[v]
            secs = sum(int(a)*b for a,b in zip(re.findall(r"(\d+)M", dur) + ["0"], [60]) ) if "M" in dur else 0
            secs += int(re.search(r"(\d+)S", dur).group(1))
            x.append(f"    <video:video><video:thumbnail_loc>{SITE}/media/{v}.jpg</video:thumbnail_loc><video:title>{html.escape(n)}</video:title>"
                     f"<video:description>{html.escape(d)}</video:description><video:content_loc>{SITE}/v/{v}.mp4</video:content_loc>"
                     f"<video:duration>{secs}</video:duration><video:publication_date>{UPLOAD}</video:publication_date></video:video>")
        x.append("  </url>")
    for lp in ("negishut","privacy","terms"):
        x.append(f"  <url><loc>{SITE}/{lp}/</loc><lastmod>{UPLOAD}</lastmod><priority>0.3</priority></url>")
    x.append("</urlset>")
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(x) + "\n")

if __name__ == "__main__":
    for p in PAGES: page(p)
    parasha_page(); patch_home(); sitemap()
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import prayers as PR
    for it in PR.P: PR.page(it)
    PR.hub(); PR.add_to_sitemap()
    import review as RV; RV.page()
    import card as CD; CD.vcard(); CD.page()
    import legal; legal.run()
    import cachebust; cachebust.run()
    print("built", [p["slug"] for p in PAGES] + ["parasha"])
