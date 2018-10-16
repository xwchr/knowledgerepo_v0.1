
STATUS_CHOICES = (
    ('draft','Draft'),
    ('reviewed','Reviewed'),
    ('review','Review'),
    ('published','Published')
)

PUB_BACKGROUNDS = (
    ('academia','Academia'),
    ('media','Media'),
    ('civilsociety','Civil Society'),
    ('government','Government'),
    ('industry','Industry'),
    ('other','Other'),
)

# publication types, taken from zotero
# https://aurimasv.github.io/z2csl/typeMap.xml
# https://www.zotero.org/support/kb/item_types_and_fields

# type ids 'attachment' and 'note' removed, type ids 'article' and 'dataset' added

PUB_TYPES = (
    ('Main', (
        ('journalArticle','Journal Article'),
        ('conferencePaper','Conference Paper'),
        ('article','Paper'),
        ('report','Report'),
        ('book','Book'),
        ('bookSection','Book Section'),
        ('newspaperArticle','Newspaper Article'),
        ('magazineArticle','Magazine Article'),
        ('blogPost','Blog Post'),
        ('webpage','Webpage'),  
    )),
    ('Other', (
        ('artwork','Artwork'),
        ('audioRecording','Audio Recording'),
        ('bill','Bill'),
        ('case','Case'),
        ('computerProgram','Computer Program'),
        ('dataset','Data Set'),
        ('dictionaryEntry','Dictionary Entry'),
        ('document','Document'),
        ('email','Email'),
        ('encyclopediaArticle','Encyclopedia Article'),
        ('film','Film'),
        ('forumPost','Forum Post'),
        ('hearing','Hearing'),
        ('instantMessage','Instant Message'),
        ('interview','Interview'),
        ('letter','Letter'),
        ('manuscript','Manuscript'),
        ('map','Map'),
        ('patent','Patent'),
        ('podcast','Podcast'),
        ('presentation','Presentation'),
        ('radioBroadcast','Radio Broadcast'),
        ('statute','Statute/Law'),
        ('thesis','Thesis'),
        ('tvBroadcast','TV Broadcast'),
        ('videoRecording','Video Recording'),
        ('other','Other')
    )),
)

def generatePubTypesPublic():
  d = {}
  for cat in PUB_TYPES:
    for t in cat[1]:
      d[t[0]] = t[1]
  d['journalArticle'] = 'Paper'
  d['conferencePaper'] = 'Paper'
  d['newspaperArticle'] = 'News article'
  return d

PUB_TYPES_PUBLIC = generatePubTypesPublic()