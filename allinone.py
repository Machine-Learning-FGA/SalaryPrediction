import math
from textblob import TextBlob as tb
import pandas as pd #manipulate csv
import csv #manipulate csv
import string #manipulate string
from collections import defaultdict #dictionary/set of words
import nltk
from nltk.corpus import wordnet


######remove columns########

def remove_columns (path, columns, newpath):
	file=pd.read_csv(path)

	keep_col = columns

	new_file = file[keep_col]

	new_file.to_csv(newpath, index=False)

	return

#####remove asterisks##############

def remove_asterisks (inp_path, out_path):
	input_file = open(inp_path, 'r')
	output_file = open(out_path, 'w')

	data = csv.reader(input_file)
	writer = csv.writer(output_file,quoting=csv.QUOTE_ALL)# dialect='excel')
	specials = '*'

	for line in data:
	    line = [value.replace(specials, ' ').lower() for value in line]
	    writer.writerow(line)

	input_file.close()
	output_file.close()

	return

#########regex find common words################

def tf(word, blob):
    return blob.words.count(word) / len(blob.words)

def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob)

def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))

def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)

def common_words (inp_path, out_path):

	input_file = open(inp_path, 'r')
	outfile = open(out_path, 'w')

	data = csv.reader(input_file)

	i = 0;

	bloblist = []
	for line in data:
		if (i == 0):
			i+=1
			continue

		s = line[1]

		bloblist.append(tb(s))


	print (len(bloblist))
	ALL = defaultdict(lambda: 0)

	j = 0
	for i, blob in enumerate(bloblist):
		scores = {word: tfidf(word, blob, bloblist) for word in blob.words if (ALL[word] == 0)}
		sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)

		j += 1
		for word, score in sorted_words[:4]:
			ALL[word] = 1
			print(word)

		if (j == 100):
			break

	input_file.close()
	outfile.close()

	return

#############merge words#################

def merge_words (f1, f2, f3, out_path):
	file = open(f1,"r")
	file1 = open(f2,"r")
	file2 = open(f3,"r")
	outfile = open(out_path, "w")
	set = {""}

	for line in file: 
		set.add(line)
	for line in file1: 
		set.add(line)
	for line in file2: 
		set.add(line)

	set = sorted(set)
	for x in set:
		outfile.write(x)

	file.close()
	file1.close()
	file2.close()
	outfile.close()

	return

##############add words as columns###############

def create_column_words (in_csv, out_csv, allwords):
	input_file = open(in_csv, 'r')

	input_file2 = open (allwords, 'r')
	ncol = sum(1 for line in input_file2)
	input_file2.close()

	input_file2 = open (allwords, 'r')	
	output_file = open(out_csv, 'w')

	data = csv.reader(input_file)
	writer = csv.writer(output_file,quoting=csv.QUOTE_ALL)

	i = 0

	for line in data:
		if i != 0:
			for i in range(0, ncol):
				line.append('0')
		if i == 0:
			for kk in input_file2:
				line.append(kk[:-1])
			i += 1

		writer.writerow(line)

	input_file.close()
	output_file.close()
	input_file2.close()

	return

######set column to 1 if word present in row##########
def find(L, target):
    start = 0
    end = len(L) - 1
    while start <= end:
        middle = (start + end)// 2
        midpoint = L[middle]
        if midpoint > target:
            end = middle - 1
        elif midpoint < target:
            start = middle + 1
        else:
            return midpoint

def setter (in_csv, out_csv, idx):

	input_file = open(in_csv, 'r')
	output_file = open(out_csv, 'w')

	data = csv.reader(input_file)
	writer = csv.writer(output_file,quoting=csv.QUOTE_ALL)

	i = 0;
	dicto = defaultdict(lambda: 0)
	finded = defaultdict(lambda: 0)
	ALLWORDS = []

	for line in data:
		if (i == 0):
			writer.writerow(line)
			for i in range(idx, len(line)):
				dicto[line[i].lower()] = i
				ALLWORDS.append(line[i].lower())
			i+=1
			continue

		abc = tb(line[1])

		for word in list(set(abc.words)): #pega todas as palavras da descriçao
			if ((find(ALLWORDS, word.lower()) == None) and (finded[word.lower()] == 0)): #se a palavra nao ta na lista das seletas
				now = wordnet.synsets(word) #pega os sinonimos da palavra atual
				achou = 0
				for syn in now: #procura cada sinonimo da palavra atual
					for l in syn.lemmas(): #no array de palavras
						if ((find(ALLWORDS, l.name().lower()) != None) or (finded[word.lower()] != 0 and finded[word.lower()] != -1)):
								line[dicto[l.name().lower()]] = 1
								finded[word] = l.name().lower()
								achou = 1
						if (achou == 1):
							break
					if (achou == 1):
						break
				if (achou == 0):
					finded[word.lower()] = -1
			elif (finded[word.lower()] != 0 and finded[word.lower()] != -1):
				line[dicto[finded[word.lower()]]] = 1
			elif (find(ALLWORDS, word.lower()) != None):
				line[dicto[word.lower()]] = 1
				finded[word.lower()] = word.lower()

		writer.writerow(line)

	input_file.close()
	output_file.close()

	return

# remove_columns ("FinalTrain.csv", ['title', 'fulldescription',  'locationraw','locationnormalized', 'salarynormalized', '\'chemistry','\'erg','\'impossible','\'laboratory','\'ll','\'re','\'s','\'shine','05','1015','11','11pm','149','1865','18th','19th','1st/2nd','2.30','200k','2012','22.00','22nd','244768','30am3:30pm','34','39','39hrs','3rd','40bedded','50bedded','55','5ft','6.51','7.40','8am6pm','9.30am5.30pm','a.s.a.p','aae','aarosetterestaurant_job','aat','abacus','abbot','aberdeen','aberdeenshire','abergavenny','abilities','about','aboveaverage','aboyne','abrecco','abta','aca/acca','access','accessing','accompanying','account','accountant','accounts','accreditation','accrington','accurate','acheive','acquired','acromas','activity','acute','addicts','address','addressed','addresses','adhd','admineclypserecruitment.co.uk','administrative','administrative/managerial','adolescent','adults','advanced','advancesteel','advisors','advisory/consultancy','aerospace','aerostructures','agents','ahg','airliners','airports','alcohol','aldershot','algorithm','allied','allocated','alloowance','all…','alnwick','already','alternate','always','amersham','anaesthetic','anaesthetics','analysers','analyses','analysis','analysis/development','analyst','analytical','anchor','andrew','anerley','angus','anlayst','ansys','anywhere','apache','apparatus','applicaitons','applications/enquiries','appointments','apprenticeships','approach','appropriate','apps','apropriate','apsley','aptitude','architecture','architectures','area.this','array','artisan','artworker','arworker','asap/excellent','asbestos','ashford','ashtonunderlyne','asp.net','asquith','assessment','assessments','assessor','asset','assignment','assistance','assistance/accompanying','assistant','assistants','assistants/support','assisted','assiting','associate/performer','associates','aston','asynchronous','athlete','attitdue','attracts','audit','auld','austell','autism','autistic','autocad','automated','automation','automotive','autonomous','availabilities','available','avalible','avanade','aviation','avon','axciting','aylesbury','ayrshire','backend','bagshot','baldock','bamber','banbury','band','bangor','bank','banks','banqueting','bar','bar/cellar','bar/waiting','barclaycard','bargoed','barnard','barnet','barnsley','barry','basell','bash','basildon','basingstoke','bath','bathe','bathgate','bay','bedford','bedfordshire','bedridden','begin','beginning','behaviours','belfast','believe','belt','benefiting','benfleet','berkshire','berkshire/buckinghamshire','betting','beverage','biannual','bid','biddable','biddulph','bideford','bigger','biggleswade','birmingham','births','bjelan','blackburn','blackpool','blank','blood','bluebird','blunsdon','bodmin','bognor','bolton','bonuses','borders','borehamwood','boss','boston','bournemouth','boutique','bowdon','bradbury','bradwell','brain','braintree','bramhope','branch','branches','breaks','brecon','breme','brent','bridport','brigade','brighton','bristol','brixton','broadcast','brokermessaging','bromich','bromley','bromsgrove','bromwich','brown','bs2573','bsc/hnc','bucks','budleigh','bulk','bursledon','burton','bushey','business','business/tenders','busy','buyouts','buzzard','bwhiskercmamail.com','c/.net','c/c','cable','cables','caerphilly','cakes','caldicott','calibre','callcentre','calorific','camberley','cambridge','cambridgeshire','camhs','campaigns','capita','capture','cardiac','cardiff','cardigan','care','care/county','careersalliedhealthcare.com','caregiver','carehome','careplanning','carer','carer/personal','carers','caring','carlisle','case','cases','cask','castle','caterham','cbm','cbt','cctv','ccw','cdp','cdps','cduttoncompassltd.co.uk','celery','cellar','cemap','centre','centred','cerebral','cfd','cfranceeclypserecruitment.co.uk','champneys','change','characterisation','charge','charing','chase','chatting','chef','chefs','chelmsford','cheltenham/gloucester','chemical','chemistry','chepstow','cheques','chesham','cheshire','chesterfield','chichester','chidren','child','childcare','childen','children','chillers','chobham','choke','choose','chorleywood','christian','chronic','churchdown','cisco','claimed','claims','clarkeholland','classical','classroom','clear','cleckheaton','click','clickonce','client','client/customer','clients','clinic','clinical','cloud','clubs','cluster','clydach','cm','cmc','cme','cms','cnc','coach','coaching','coastal','coding','colchester','collaboration','colleagues','com/dcom','commandline','commercial','commis','commissioning','commited','commitment','commitmentshowever','committment','commode','communications','community','comorbidities','companionship','company.based','companyfunded','compass','compassionate','compensation','competitor/industry','complemented','compliance','complications','component','composite','comprehension','computing/software','con/sol','conceptual','condition','conformance','construction','consultancy/outsourcing','consultancy/strategy','consultant','consultants','consultations','consumables/office','control','controls','controlsrelated','cooking','cooks','cool','cooling','coordinated','coordinator','copd','cordinator','cote','cough','could','counties','county','course','court','cousins','coventry','coventry/warwickshire','cowbridge','cqc','craving','crb','crew','criteria','critical/urgent','crm','cropped','crossbrowser','crossfunctional','crossinfection','crossselling','croxley','crussellcompassltd.co.uk','csr','cumbria','custodial','customer','customers','customs','cvinterviewplacement','cwmbran','cycles','d.williamsedenbrown.com','d36','daily/weekly','daniel.thompsonsynergygroup.co.uk','danish','danish/dutch/french','danish/dutch/french/german','dashboards','dataserver','davenham','daventry','daycase','days/nights','deane','decided','decisions','declarations','decommissioning','decomposition','deescalation','defence','defence/communications','deliverables','delivery/customer','delphi','dementia','demi','demi/cdp','demonstrates','demonstrating','denaby','dental','dentist','dependencies','deployments','deputy','derbyshire','derry','descriminatory','design','design/construction','design/test','designer','designs','desk','desktop','detention','determined','detox','developer','developer/designer','developers','development','development/electronic','developments','devising','devon','diabetes','diagrams','diamond','diesel','difficulties','digital','dihatsu','dimensions','dinas','dining','diploma','director','disabilites','disabilities','disability','disabled','discharges','disciplinaries','disclosure','disclosures','discrepant','discriminate','dishes','disorder','disorders','dispensary','display','dissabilities','distribution','distributor','dlangfordcompassltd.co.uk','docare','documentation','dolphin','domains','domestic','domiciliary','domicilliary','doncaster','door','doors','dorking','dorset','doubles','dovetail','drafting','drama','dream','drink','driver','droylsden','drupal','dsp','dubai','dublin','dudley','dumfries','dundee','dundee/angus','dungannon','dunmow','dunstable','durham','dursley','dutch','duties','dvbt','east/africa/latin','eastleigh','eastwood','easyfit','ebucklecompassltd.co.uk','echadwickeclypserecruitment.co.uk','eclipse','eclypse','ecological','ecology','ecommerce','eden','edinburgh','education','effectiely','ejb','elaborating','elderley','elderly','elderly/dementia/physically','elearning','electrical','electromechanical','electronic','electronic/electrical','electronics','element','elina.grigorjevaactiveassistance.com','elmbridge','email/call','email/calls','embedded','emc','emea','emma.bjelansynergygroup.co.uk','emodule','emotional','employer.hertsmere','enablement','encouraging','endoflife','endoscopic','endoscopy','energy','enfield','engage','engineer','engineer/technical','engineering','engineers','english','enjoy','enjoys','enrich','ensures','ent/ophthalmic','ent/ophthalmic/maxilla','enteral','enterprisewide','environmental','epilepsy','epsom','equipment','equipment/supplies','erdington','escorts','esmitheclypserecruitment.co.uk','essex','establishment','establishments','estate','esturgesscompassltd.co.uk','etc','european','euros','evaluation','eve.lethbridgeappointgroup.co.uk','evenings','events','everyday','evesham','evidence','exams','excise','executive','exeter','expense','experianced','experinece','experirnce','explore','exponentiale','export','exports','extra','extrusion','extrusions','eyfs','fabrications','fabricators','facilitiy','facilty','facing','falkirk','famed','families','family','famous','fanac','fareham','faria','faria.zahidjustsocialcare.co.uk','farnborough','farnham','fatigue','faversham','fb','fea','feasibility','features','female','femco','ferryhill','fertilisation','fertility','fft','field/oil','fieldwork','fife','finance','financial','finch','findon','finish','finite','finnish','firm','fitness','fitters','flashbuilder','flat','fleet','flexiable','flexibile','floating','flotation','fluent','folkestone','food','foodie','football','forbes','forecasting','foreign','fortran','fourier','frail','frameworks','french','fresh','friendship','frizzell','front','frontline','fsa','fuelphp','fulbourn','fulfilment','fundraising','fundtech','fx','galloway','gamble','games/social','garelochhead','gas/subsea','gastro','gastrostomy','gathering','gbp/hr','gchq','general','gentleman','gentlemen','george','german','germanspeaker','giver','glasgow','glossop','gloucester','gloucestershire','gmc','goals','gosport','governance','gp','grades/levels','graduate','graduates','grampians','graphics','gravesend','great','greater','grehrcompassltd.co.uk','grievancestupeunionsexperience','griffin','grinder','group','growths','gscc','gscc/hcpc','gss','guest','guests','guidelines','guidelines.participate','guides','guildford','guinness','gymnastic','gymnastics','gymnstics','gynaecology','h1','half','halifax','halwill','hammersmith','hampshire','hams/torquay/teignmouth','handling','handson','hants','happiness','happy','harassment','hardware','harrogate','harrow','harrowgate','hartlepool','haven','having','hay','hazardous','hci/je','hdc','hdu','head','headhunting','health','healthcare','hearing','hebrew','help','helpful','helping','hempstead/three','hereford','herefordshire','herne','hertford','hertfordshire','herts','hertsmere','hexham','hgv','highland','highlands','highlyskilled','highrevenue','hillingdon','hillyard','hingham','histon','hmgcc','hnc/onc','hobbies','holder','home','home.a','homecare','homes','homeworking','hopwood','horeca','hospital','hospitals','hospitasl','hotel','hotel.in','hotels','houghton','hours/nights','housekeeper','housework','housing','hove','hpc','hr','hr/payroll','hse','hsqldb','html/css/js','huddersfield','hull','huyton','hydrographic','hygiene','hygienist','iapt','icu/theatres','ideals','identify','idts','iee','igloo','ileostomy','ilford','ilfracombe','ilkeston','ilkley','illegal','illness/personality','illnesses','illogan','impairments','impeccably','impending','impington','implanters','implementation','implementer','impulse','inbound/outbound','incentives','incremental','independence','individualised','individuals','industrial','inevitably','influencers','information.hays','infrastructure','ingredients','initialise','initiatives.the','initio','injection','injuries','injury','inns','inpatient','input','inspire','installation','installs','instructions','instrumentation','insurance','integral','integration','integrity','intelligent','intensity','intensive','intention','interaction','interactions','interests','interlock','intermittent','interpreting','intervention','interventions','intuitive','inverness','inverurie','investigations','investment','investor','invitations','iopen','ios','ipswich','irse','iseb','isle','it/office','it/technical','italian','itil','ives/penzance/redruth','ivf','jag','jamie','japanese','java','java/j','javascript','jeffwhiterecruitment.com','jevansbondrecruitment.com','jforbescompassltd.co.uk','jkempcompassltd.co.uk','jobsuniversalmedics.co.uk','jodie','johns','johnson','jonaddisonfowle.co.uk','joomla','jrh','judicious','juggle','junior','just','justification','justnursing','jwildscompassltd.co.uk','k.stockedenbrown.com','kare','kberrycompassltd.co.uk','keighley','kelly','kenley','kent','keynes','keyworth','kickstartsynergygroup.co.uk','kidderminster','kidsgrove','kingswinford','kinross','kirkby','kirklees','kitchen','kitchen.an','kitchens','knowledge/experience','knowledgeable','kodak','kpmanchesterkareplus.co.uk','ks1','ks2','kv','kwestsussex_job','kylie','l.stevensedenbrown.com','laboratory','labour','labview','ladder','lady','laminates','lanarkshire','landlords','langford','language','languages','laparoscopic','laprascopic','larder','launch','launching','laundry','lead/medicines','leader','leader/sister','leadership','leads','learning','leaving','ledger/credit','leicester','leicestershire','leighton','lending','lettings','lewis','lewy','leyland','lgv','liasing','licence/own','licenced','license','licensing','lichfield','life','lifecarers','lifestyle','lifton','lincoln','lincolnshire','linux','linux/unix','lisence','livein','liverpool','living','llangollen','llanrumney','llminster','lmc','loans','located','locations','locum','longton','look/feel','looked','lookout','losbornecompassltd.co.uk','lothian','loughborough','louth','lowestoft','lowestoft/great','lrs','lunchtimes','luxurious','luxury','lydia','lydia.robinsonappointgroup.co.uk','lyme','lync','lyneham','m25','machine','machinery','machines','maestag','maidstone','mainland','maintenance','male/female','managed','management/registered','manager','manager/elderly','manager/qcf','managerial','managerially','managers/partners','manchester','mandatory','manitenance','mansfield','manufacturing','marcia','margate','maricare','marketing','markets.they','marlown','marston','mathcad','mathematical','mathematics','mature','maybe','mcad','mcdowell','meals','mechanical','medacs','medical','medication','medications','meeds','megan','membership/cms/hr/payroll/email/fundraising','mental','mentioned','menu','menus','meritocratic','merrygoround','merseyside','merthyr','metallic','methodologies','mfc','mice','michelin','microbiology','microcontrollers','microp','microsoft','middlesbrough','middlesex','middleton','midhurst','midlands.•excellent','midsize','midweight','midwife','mileage','milford','military','miller','milton','minimise/eliminate','minimum','minor','miser','misuse','mixed','mnd','modeller','modelling','mondayfriday','mondayfridayif','monitoring','monmouth','monthly','morecambe','mornings/lates','mortgage','moston','motivation/enthusiasm/flexibility','mottram','moulding','mountain','mrcp','mri/ct','msmq','multidiscipline','multimeters','multinational','multiserver','multisite','multithreaded','multitude','musculoskeletal','mutlimillion','mvc','mvc/asp.net','mvt','mvvm','mwilkinsoncompassltd.co.uk','my','n.yorks','nantwich','nationwide','natiowide','necessary.assess','needs','negotiator','net','networking','neurology','neurology/neurosurgery','neurons','neurosurgery','newbury','newcastle','newcastle/north','newent','newport','newton','nhs','nhs/private','night','nights','nii','nmc','noninfrastructure','nonmedical','nonregulated','nonsmoker','nonthreatening','norfolk','northampton','northamptonshire','northants.the','northumberland','northwich','norwegian','norwich','nottingham','nottinghamshire','november','novus','nuclear','numerous','nures','nurse','nurse/endoscopy','nurse/odp','nursery','nurses','nurses/odp','nursing','nurturing','nutrition','nvq','objectoriented','obsession','obtaining','obviously','occupational','odp','ofconsistent','offending','offering','offers','officer','offline','offshore','ofoffers','ofsted','oh','oil','oiled','oldham','olga','olympics','onboarding','online','only.in','operating','operation.a','operational','operations','operations.a','ophthalmology','oppurtunity','optimsiation','orderly','orders','organisation.hays','oriented','orthapaedics','orthopaedic','orthopaedics','orthpaedic','os/x','osborne','oscilloscopes','outbound','outgoing','outings','outline','outpatients','outreach','overdrive','owner/driver','oxford','oxfordshire','oxted','p.a','p.beneferedenbrown.com','p.hr','p/hr','paediatric','paeds','paignton','paisley','pallative','palliative','palsy','palsy/epilepsy','parallel','parameterised','paresis','participate','partie','parties','partly','partqualified','passport','passport/driving','pastry','patient','patients','payments','payoff','payroll','pcs','pds','peform','peg','pegs','pembrokeshire','people','people/customer','performance','perks','perl','permanents','persistance','personal','personality','personnel','persons','pertemps','perth','perthshire','peterborough','peterhead','phamaceutical','pharmaceutical','pharmacist','pharmacy','phase','philosophy','photographers','photolith','php','php/.net/python','physical','physiotherapist','picturesque','piercing','piggy','pilpulsejobs.com','pioneeer','pioneer','pitlochry','plans.the','plastic','plastics','platers','platform','platofrm','playback','plc/scada/ica','plymouth','polebrook','policy','policy.administer','pontypridd','pool','poole','popular','portfolios','portsmouth','positionsupport','postions','potential','power','powershell','powys','ppc','practice','practiced','practising','practitioner','practitioners','precision','preconcept','pregnancy','prepper','presales','presnst','pressuremethodical','preston','pricings','primary','primavera','principal','print','printing','prison','prisoners','prisons','private','privelege','privilege','privileged','problems','procedures','proceedings','process','processing','procurement','produce.all','production','professionalism','profiler','programmer','programmes','project/chief','projects','projects.hays','proof','property','proprietor','prorota','protect','protection','provides','psls','psp','pspice','psychiatrists','psychiatry','psychological','psychologically','psychologists','pub','pulse','punjabi','pupils','purchasers','purchasing/objectives','pwp','qlikview','qsw','qualified','qualified/late','qualified/newly','quality','quality.a','quality/regulatory','quality/safety','quotation','quotations','r.allinsonedenbrown.com','radiographer','radiography','radiopharmaceutical','raes','railway','rainham','ramification','ranges','rasen','rcgp','rdbms','reading/basingstoke','real','realtime','rebate','receives','recent','reconciliation','records','recovery','recreations','recruitment','recs','recuiting','redditch','redhill','refrigeration','refurbishment/rekit','region','regional','registered','registration','registration/practitioner','rehr','rejected','rejects','relative/friend','relaxation','reliability/punctuality','relief','religious','relying','remain','remedy','rendlesham','renfrewshire','reporting','repositioning','reprioritisation','reputed','requests','required.this','requiredconcept','research','residentail','residential','residential/nursing','residents','resort','resourcing','respiratory','responsbile','restarant','restaurant','restaurant.in','restaurant.the','restoration','resultant','retailers','retrieval','revenue','reviewing','reviews','revpar','rgn','rgn/odp','rgn/rmn','rgns','rh5','rhapsody','rhct','rhymney','rickmansworth','right','righthand','rights','ripley','risk','rmn','rmn/rnld','rmns','rnld','rnmh','roadshow','rochester.both','rooms','rooms.in','roseete','rosette','rosettehotelnyorks','rosettekitchenupto','rosettes','rosettes.all','rostering','rotate','rotation','rotisserie','royston','runnymede','runout','rushhour','rushmoor','russian/polish','s.leighedenbrown.com','sa/etl','safeguarding','safety','saga','sage','salaried','salary','sales','sales/account','salesjobscitycareers.com','salford','salterton','sanctuary','sandwich','sandy','sap','satisfacftion','satisfy','sauce','savings/service','sbs','scarborough','sccm','scheduler/emergency','schematics','school','schools','scientific','scotland','scousinscompassltd.co.uk','screening','scrub','scswis.we','seals','seaton','secondary','section.this','sector/dementia','secure','security','seekers','segregating','selection','selenium','selfinitiated','selflearner','selfmotivated','selfstarting','sellafield','semi','semiautonomously','sending','senior','seniors','sensory','seo','seperate','server','servers','service.a','service/support','services','services/soap/xml','servicespecific','serviceusers','setter','sevenbedded','sharepoint','shares','sharnbrook','sharptext','sheffield','shefford','sherborne','shields','shifts','shipley','shopfitting','shoreham','showrounds','shrunk','sidmouth','sigma','silchester','silsden','simulation','sister','sitters','six','sized','sizing','skegness','skillls','skills/knowledge','skills/responsibilities','sleep','sleeping','slideways','slimbridge','smart','smethwick','smooth','snacks.at','so.all','social','socialising','socializing','socks','soe','softer','software','soiled','solicitors','solihull','solutioning','solutions','somebody','someone','somerset','sonar','sosa','sous','south','southampton','southend','southern','southport','southwark','spa','spanish','spark','sparql','speaking','specialist','specialities','specialties','species','specification','spelthorne','spending','spinal','sport','sporting','springing','sproutcore','sql','square','staff','staffing','staffordshire','stage','stalybridge','stamps','staplehurst','stars','static','statistical','statistics','steel','steelwork','stepping','steria','sterilisation','sterilising','stevenage','stevens','stiffness','stimulation','stirling','stl','stockholders','stockport','stocks','stockton','stoke','stoma','stomacare','storage','stornaway','strategic','strathclyde','streamuk','stress','stressful','stretching','stronger','structural','structural/stress','structure.where','structures','studies','studio','studios','sturgess','subscribers','subsea','substance','substances','substantiation','substations','succesful','such','suctioning','suffered','suffolk','sunderland','superb','supernumerary','superstars','supervisory','supewervised','support','supported','surgery','surgical','surgury','surrey','surronding','surrounded','surrounding','surveillance','survey','sussex','sutton','svq','swanage','swansea','swanstaff','swimming','swt','sybase','syd','synarbor','synergy','syringe','systems','taking/logging','takisawa','talbot','tameside','tamsin','tara','taraclearselection.co.uk','tasked','taunton','taverns','tayside','tcp/ip/udp','teacher','teachers','teaching','team/s','technical','technician','techniques.the','technologically','technologies','teddington','teenage','tees','tekdata','telecoms','teleconferences','teleconferencing','telemarketing','telemedicine','telesales','telford','telling','tenders','tenterden','terms','test','testbeds','testing','tewkesbury','tfidf','thatcham','theatre','therapeutic','therapists','therapy','thetford','theuk','threaded','thresholds','thurrock','tidy','time/permanent','timeline','tintwistle','tiny','tipsbenefits_job','tipton','tiptop','tla','tooling','toolmaker/quality','torbay','tornos','torquay','tots','tough','trachea/vent/cough','tracheaostomy','traffic','trafford','trainer','trainers','training','trampolining','transaction','transfer','transition','transitioning','transitions','translation','translations','translator','transmission','treasury','treats','treherbert','trent','triage','trials','triathlon','tribunal','trident','tunbridge','turriff','tw/256','tydfil','tyne','tynedale','tyneside','tyrone','uckfield','uda','uiform','ukcourses','umbilical','uml','unbeatable','undergoes','underwater','undiagnosed','undifferentiated','unified','unioon','universal','unlimited','unobstructed','unprecedented','unwell','upfront','uppingham','urgently','usefulness','users','uttoxeter','v.net','v1','vaccinations','validation','values','valuing','valve','valves','vanrath','varied','variety','vb.net','vba','vendor','venue','verification','verwood','vessels','video','village','vpls','vulnerable','wadhurst','wage','waiting','waking','waldrich','wales','walsall','ward/department','wareham','wargaming','warranty','warwickshire','washing','washington','water','waterpolo','watershed','watford','watford/hertsmere/three','watfords','wealth','weapon','web','web/application','web/graphic','webbased','webcasting','webscale','website','weddings','wednesbury','weekends/evenings','welding','wellbeing','wellington','wellness','wells','welwyn','west','westbourne','westerham','westminster','weymouth','when','while','white','whittlebury','whom','why','wide','widnes','wight','wilkinson','williams','wilmslow','wiltshire','winchester','windows/iis','winforms','winkleigh','winner','wirral','wisely','wishing','withchildren','woking','wokingham','wolverhampton','wombourne','women','worcester','worcestershire','worked','worker','workers','workflow','workington','wormelow','worthing','writtenexplain','wroughton','wsse','www.bluebirdcare.co.uk/trafford','www.bluebirdcare.co.uk/weymouth','www.brunningandprice.co.uk','www.caterer.com/jobseeking/assistantmanagernearessexfreshfoodpubupto','www.caterer.com/jobseeking/assistantmanagersuffolkcoastalrestaurant','www.caterer.com/jobseeking/chefdepartieawardwinningdiningliveinshareoftips_job','www.caterer.com/jobseeking/chefdepartieawardwinningfinediningrestaurantstraights_job','www.caterer.com/jobseeking/chefdepartieawardwinningrestaurantexcellenttips_job','www.caterer.com/jobseeking/chefdepartieburtonontrentupto','www.caterer.com/jobseeking/chefdepartiecharminghotelallfreshfoodtipslivein_job','www.caterer.com/jobseeking/chefdepartieexceptionalawardwinningrestaurantservicecharge_job','www.caterer.com/jobseeking/chefdepartiehighqualityhotelfreshinternationalcuisine_job','www.caterer.com/jobseeking/chefdepartiehighvolumefreshfoodpubshareoftips_job','www.caterer.com/jobseeking/chefdepartienorfolkliveinupto','www.caterer.com/jobseeking/chefdepartieorstrongdemi_job','www.caterer.com/jobseeking/chefdepartiepositionin','www.caterer.com/jobseeking/chefdepartiesauceawardwinninghertford','www.caterer.com/jobseeking/chefdepartiesmallfoodfocusedhotelallfreshtips_job','www.caterer.com/jobseeking/chefdepartiesrequirednationwidemanywithlivein_job','www.caterer.com/jobseeking/chefderanghighprofile','www.caterer.com/jobseeking/clientaccountexecutive_job','www.caterer.com/jobseeking/clusterrevenuemanager_job','www.caterer.com/jobseeking/commischefawardwinningprivatelyownedrestaurantfreelivein_job','www.caterer.com/jobseeking/commischeflargehotelwithexcellentcareerprospectsfreshfood_job','www.caterer.com/jobseeking/commischefleadingrestaurantoffsiteliveinshareoftips_job','www.caterer.com/jobseeking/commischefluxurioushotelfinediningrestaurantlivein_job','www.caterer.com/jobseeking/commischefopenplankitchenbrasserierestaurantlivein_job','www.caterer.com/jobseeking/countlessfreshfoodchefpositionsnationwide','www.caterer.com/jobseeking/finediningchefsforrosetterestaurantsupto','www.caterer.com/jobseeking/generalmanagerbeautifulhotel_job','www.caterer.com/jobseeking/generalmanagerfunkycoolrestaurantconceptlondon','www.caterer.com/jobseeking/headchefnottinghamareabrandedrestaurantsalaryote','www.caterer.com/jobseeking/juniorsouschefrelaxedcountrypuballfreshfoodtips_job','www.caterer.com/jobseeking/keyaccountmanager_job54201896','www.caterer.com/jobseeking/micesalesandmarketingmanager_job','www.caterer.com/jobseeking/pastrychefal','www.caterer.com/jobseeking/pastrycheffoodledpubaaaccreditedrestauranttipslivein_job','www.caterer.com/jobseeking/pastrycheffor','www.caterer.com/jobseeking/pastrychefmultiaarosettehotelleadingateamfreelivein_job','www.caterer.com/jobseeking/reliefchefdepartiecroydonsurreylivein_job','www.caterer.com/jobseeking/revenuemanagerluxuryresorthotelspaliveinavailable_job','www.caterer.com/jobseeking/seniorsouscheffor','www.caterer.com/jobseeking/seniorsouschefgastropub','www.caterer.com/jobseeking/welwynchefdepartiedoesitgetanybetterthanthis','www.clearselection.co.uk/search.php','www.cmcconsulting.co.uk','www.docare.co.uk/forms/jobapplication','www.h1healthcare.com/register.html','www.kirkleesactive.co.uk','www.totaljobs.com/jobseeking/meoperationsmanager_job','wycombe','xamp','xml/xsl','xrf','yarmouth','yearend','yeovil','york','yorkshire','yos','young','youth','yrs','ystaltfera','ystradgynlais','zahid','zero','–','’','•','•great','•maintain','€','conducting','commercial','risk'], "FinalTrainFixdColumns.csv")
# remove_columns ("Test_rev1.csv", ['Title', 'FullDescription', 'LocationRaw', 'LocationNormalized', 'ContractType', 'ContractTime', 'Company'], "TestFixdColumns.csv")
# remove_columns ("Valid_rev1.csv", ['Title', 'FullDescription', 'LocationRaw', 'LocationNormalized', 'ContractType', 'ContractTime', 'Company'], "ValidFixdColumns.csv")

# remove_asterisks ("TrainFixdColumns.csv", "TrainFixdAsterisks.csv")
# remove_asterisks ("TestFixdColumns.csv", "TestFixdAsterisks.csv")
# remove_asterisks ("ValidFixdColumns.csv", "ValidFixdAsterisks.csv")

# common_words ("TrainFixdAsterisks.csv", "train.txt")
# common_words ("TestFixdAsterisks.csv", "test.txt")
# common_words ("ValidFixdAsterisks.csv", "Valid.txt")

# merge_words ("train.txt", "test.txt", "Valid.txt", "allwords.txt")

# create_column_words ("TrainFixdAsterisks.csv", "TrainWithColumns.csv", "allwords.txt")
# create_column_words ("TrainFixdAsterisks.csv", "TrainWithColumns.csv", "allwords.txt")
# create_column_words ("TestFixdAsterisks.csv", "TestWithColumns.csv", "allwords.txt")

# setter ("TrainWithColumns.csv", "FinalTrain.csv", 8)
# setter ("TestWithColumns.csv", "FinalTest.csv", 7)
# setter ("ValidWithColumns.csv", "FinalValid.csv", 7)
