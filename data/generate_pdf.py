"""
Generator script to produce the 50-page historical archival document using PyMuPDF (fitz):
data/indian_railways_and_telegraph_history_50p.pdf

Titled: Modern History & Archival Chronicle: Indian Railways and Telegraph System (1845-1900)
"""

import os
import fitz  # PyMuPDF

def clean_text(s: str) -> str:
    """Replace non-ASCII quotation marks and dashes with standard ASCII equivalents."""
    return (s.replace("–", "-")
             .replace("—", "-")
             .replace("‘", "'")
             .replace("’", "'")
             .replace("“", '"')
             .replace("”", '"'))

def insert_autofit(page, rect, text, max_fs=12, min_fs=8, fontname="helv", color=(0, 0, 0), align=0):
    text = clean_text(text)
    for fs in [max_fs, max_fs - 0.5, max_fs - 1.0, max_fs - 1.5, max_fs - 2.0, min_fs]:
        res = page.insert_textbox(rect, text, fontsize=fs, fontname=fontname, color=color, align=align)
        if res >= 0:
            return res
    return page.insert_textbox(rect, text, fontsize=min_fs, fontname=fontname, color=color, align=align)

def build_pdf(filename="data/indian_railways_and_telegraph_history_50p.pdf"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    doc = fitz.open()
    
    # 50 pages of structured historical archive content
    pages_content = [
        # Page 1: Title & Archival Frontispiece
        [
            ("TITLE", "Modern History & Archival Chronicle Assistant"),
            ("SUBTITLE", "Documentary Series: Indian Railways and the Electric Telegraph System (1845-1900)\nArchival Chronicle & Official Records Compilation"),
            ("BODY", "This archival collection compiles primary colonial dispatches, legislative proceedings, engineering survey reports, and telegraphic logs tracing the modernization of transport and telecommunications across the Indian subcontinent between 1845 and 1900."),
            ("BODY", "Preserved within the records of the Public Works Department, the Railway Branch, and the Home Department of the Government of India, these fifty folios establish the administrative frameworks, technical hurdles, financial contracts, and geopolitical imperatives that guided early Victorian infrastructure."),
            ("BODY", "The dual introduction of the iron road and the electric wire in the 1850s transformed the spatial geography of South Asia, radically altering commerce, military mobilization, revenue administration, and famine management under East India Company rule and subsequent British Crown governance."),
            ("BODY", "Archival Reference: IOR/L/PWD/3/1849-1895. Published under archival authority for scholarly examination, textual verification, and historical chronicle retrieval.")
        ],
        # Page 2: Table of Contents & Archival Index
        [
            ("HEADER", "Archival Index and Table of Folios"),
            ("BODY", "Folio 3-5: Chapter 1 - The Genesis of Indian Railways and the 1849 Guarantee System\n\n"
                     "Folio 6-8: Chapter 2 - The First Iron Wheels: Bombay to Tannah (1850-1853)\n\n"
                     "Folio 9-11: Chapter 3 - The Bhor Ghat Incline: Engineering Obstacles and Reversing Stations\n\n"
                     "Folio 12-14: Chapter 4 - The Electric Telegraph: Dr. O'Shaughnessy and the Diamond Harbour Line\n\n"
                     "Folio 15-16: Chapter 5 - Lord Dalhousie's Railway Minute and the Trunk System (1853)\n\n"
                     "Folio 17-18: Chapter 6 - The Great Indian Peninsula Railway: Early Expansion\n\n"
                     "Folio 19-20: Chapter 7 - The East Indian Railway: Howrah to the Coalfields\n\n"
                     "Folio 21-22: Chapter 8 - The Madras Railway and Southern Corridors\n\n"
                     "Folio 23-25: Chapter 9 - Transcontinental Telegraph Lines: Calcutta to Agra and Bombay\n\n"
                     "Folio 26-28: Chapter 10 - The 1857 Uprising and the Strategic Role of Communications\n\n"
                     "Folio 29-30: Chapter 11 - The Thul Ghat Ascent: Comparative Mountain Engineering\n\n"
                     "Folio 31-32: Chapter 12 - Lord Lawrence and the State Railway Experiment (1869-1880)\n\n"
                     "Folio 33-34: Chapter 13 - Indo-European Submarine Cables and the Persian Gulf Line\n\n"
                     "Folio 35-36: Chapter 14 - Famine Relief Commissions and Protective Lines\n\n"
                     "Folio 37-38: Chapter 15 - Block Signaling and Technical Safety Mechanisms\n\n"
                     "Folio 39-40: Chapter 16 - Locomotive Workshops: Jamalpur, Parel, and Perambur\n\n"
                     "Folio 41-42: Chapter 17 - Frontier Railways: Sind, Punjab, and Bolan Pass\n\n"
                     "Folio 43-44: Chapter 18 - Commercialization of Telegraphy and Tariff Reforms\n\n"
                     "Folio 45-46: Chapter 19 - The Modified Guarantee Contracts of the 1880s\n\n"
                     "Folio 47-48: Chapter 20 - Economic Transformation, Market Integration, and Historiography\n\n"
                     "Folio 49-50: Archival Documentary Transcripts and Chronological Appendices"),
            ("BODY", "Notice to Researchers: All textual verifications must rely exclusively on the certified records transcribed herein. No supplementary assumptions or unrecorded modern claims shall be admitted into archival findings.")
        ],
        # Page 3: Chapter 1 - Genesis of Indian Railways
        [
            ("HEADER", "Chapter 1: The Genesis of Indian Railways (1845-1848)"),
            ("BODY", "The initial proposals for establishing steam locomotion across British India originated in London commercial circles during the early 1840s. Proponents argued that regular rail transportation would unlock raw cotton exports from the interior, ensure rapid troops transit to vulnerable frontiers, and diminish the prohibitive costs of bullock-cart transit along unpaved tracks."),
            ("BODY", "In 1845, the East Indian Railway Company (EIR) was formed in London under the directorship of Rowland Macdonald Stephenson. Concurrently, in western India, John Chapman organized the Great Indian Peninsula Railway Company (GIPR) with the support of prominent British merchants and Bombay merchant prince Sir Jamsetjee Jejeebhoy."),
            ("BODY", "However, private investors in London refused to commit capital to perilous subcontinental ventures without sovereign financial insulation. The Court of Directors of the East India Company initially hesitated, citing fiscal caution, unpredictable monsoon downpours, and termites. Negotiations dragged on for four years between 1845 and 1849 over the specific financial guarantees required to draw British private capital.")
        ],
        # Page 4: Chapter 1 (cont.) - The 1849 Contract Terms & Guarantee Rate
        [
            ("HEADER", "Chapter 1 (Continued): The 1849 Contracts and the Old Guarantee System"),
            ("BODY", "On August 17, 1849, the historic contract terms were formally signed in London between the East India Company and the pioneer railway companies - the East Indian Railway Company and the Great Indian Peninsula Railway Company."),
            ("BODY", "Under the formal terms of the 1849 contract, the colonial administration promised private British railway companies an exact annual guaranteed interest rate of 5% (five percent), expressed as a fixed return on all subscribed capital invested into line construction. This arrangement was known as the 'Old Guarantee System'."),
            ("BODY", "The contract stipulated that should operating net profits fall short of 5%, the deficit would be paid directly from the public revenues of British India. Furthermore, the colonial administration agreed to provide all land required for the permanent way free of cost on a 99-year lease. If profits exceeded the 5% threshold, the surplus was to be split equally between the private enterprise and the government."),
            ("BODY", "This generous 5% annual guarantee completely eliminated financial risk for British capitalists, encouraging an immediate influx of British sterling into Indian railway bonds, while placing the entire contingent tax liability upon Indian taxpayers.")
        ],
        # Page 5: Chapter 1 (cont.) - Financial Mechanisms & London Share Markets
        [
            ("HEADER", "Chapter 1 (Continued): Capitalization and Debenture Issuance"),
            ("BODY", "Following the ratification of the 1849 contract, subscriptions for Indian railway shares opened on the London Stock Exchange with immediate oversubscription. British investors, accustomed to domestic railway returns of only 3 to 4 percent, viewed the 5 percent Indian sovereign guarantee as an unassailable financial haven."),
            ("BODY", "The capital was raised entirely in sterling and deposited with the East India Company treasury in London. The colonial administration then made funds available in rupees in Bombay and Calcutta at a guaranteed exchange rate of 1 shilling and 10 pence per rupee, further shielding investors against foreign exchange depreciation."),
            ("BODY", "Critics in both Parliament and India noted that this risk-free 5% return fostered lavish, unchecked expenditure. Because companies were guaranteed 5% on whatever capital they disbursed, there was little incentive to economize on brickwork, iron bridge spans, or administrative salaries, leading Lord Dalhousie to institute strict government engineering oversight.")
        ],
        # Page 6: Chapter 2 - The First Iron Wheels: Bombay to Tannah
        [
            ("HEADER", "Chapter 2: The First Iron Wheels - Bombay to Tannah (1850-1853)"),
            ("BODY", "Survey operations for the Great Indian Peninsula Railway commenced in 1850 under the direction of Chief Engineer James John Berkley. The chosen initial alignment ran from Bori Bunder in Bombay across the Salsette island to the ancient port town of Tannah (Thane), spanning a distance of 21 miles."),
            ("BODY", "Construction of this first experimental line commenced in 1851. Over 10,000 local laborers were engaged to level causeways, excavate cuttings through basalt rock, and lay ballast across marshy flats. British iron rails weighing 65 pounds per yard were imported by sailing vessels around the Cape of Good Hope."),
            ("BODY", "Contractors Messrs. Favell and Fowler supervised track-laying, while rolling stock was shipped in parts from Vulcan Foundry in England. Despite unseasonal rains and outbreaks of malaria, the line was completed for trial runs in early 1853.")
        ],
        # Page 7: Chapter 2 (cont.) - The Inaugural Run of April 16, 1853
        [
            ("HEADER", "Chapter 2 (Continued): The Historic Departure at Bori Bunder"),
            ("BODY", "On the afternoon of Saturday, April 16, 1853, the first commercial passenger train in India made its historic journey. At 3:30 PM, amidst a 21-gun salute and the cheers of thousands of spectators, the train departed Bori Bunder station bound for Tannah."),
            ("BODY", "The train consisted of 14 passenger carriages carrying approximately 400 distinguished guests, including colonial administrators, military officers, and Indian merchants. The train was hauled by three steam locomotives manufactured by Vulcan Foundry, christened 'Sindh', 'Sultan', and 'Sahib'."),
            ("BODY", "Covering the 21-mile distance in 57 minutes, the train reached Tannah at 4:27 PM to euphoric public acclaim. The successful journey demonstrated the mechanical viability of railways in the Indian climate and inaugurated an era of aggressive rail expansion across the subcontinent.")
        ],
        # Page 8: Chapter 2 (cont.) - Public Reception & Traffic Growth
        [
            ("HEADER", "Chapter 2 (Continued): Early Operating Results and Native Patronage"),
            ("BODY", "Following the inaugural run, regular passenger services commenced on April 18, 1853. Contrary to European predictions that caste distinctions and religious customs would deter high-caste and low-caste Hindus from sitting together in common compartments, native patronage was instantaneous and overwhelming."),
            ("BODY", "In the first month alone, over 70,000 passengers purchased tickets across three classes of travel. Third-class fares were fixed at approximately 3 pies per mile, enabling ordinary artisans, peasants, and merchants to travel at speeds previously unimagined."),
            ("BODY", "The economic success of the Bombay-Tannah section validated the GIPR's plans to extend the line beyond Kalyan, where the railway split into two ambitious branches: the North-Eastern line toward the Thul Ghat and the South-Eastern line toward the formidable Bhor Ghat.")
        ],
        # Page 9: Chapter 3 - The Bhor Ghat Incline & Engineering Obstacles
        [
            ("HEADER", "Chapter 3: The Bhor Ghat Incline - Engineering Obstacles and Reversing Stations"),
            ("BODY", "In Chapter 3 of the archival records, Chief Engineer James John Berkley detailed the supreme mechanical challenge confronting the GIPR South-Eastern line: ascending the Sahyadri range of the Western Ghats between Palasdhari and Khandala to connect the Bombay coast with the Deccan plateau at Pune."),
            ("BODY", "The primary engineering obstacle on the Bhor Ghat incline that made the reversing station necessary was the sheer, precipitous rocky cliff and abrupt mountain ascent of the Western Ghats escarpment, which rose over 1,800 feet within a compressed horizontal distance of barely 15 to 16 miles. A direct straight ascent would have produced an impossibly steep gradient beyond the adhesion limits of 19th-century steam engines."),
            ("BODY", "To surmount this formidable obstacle without exceeding mechanical tractive safety, Berkley designed an ingenious switchback reversing station at Khandala. Under this configuration, trains ascended to a dead-end spur, halted, reversed direction, and ascended the next inclined tier. The gradient ratio on the steepest sections of the Bhor Ghat incline was 1 in 37 (with a ruling average gradient ratio of 1 in 40 along the general ascent)."),
            ("BODY", "This gradient ratio of 1 in 37 required specialized brake vans and heavy tank engines. Without the reversing station, scaling the sheer mountain cliff of the Ghats would have been impossible for contemporary locomotive technology.")
        ],
        # Page 10: Chapter 3 (cont.) - Construction Trials on the Bhor Ghat
        [
            ("HEADER", "Chapter 3 (Continued): Blasting Basalt and Labor Casualties"),
            ("BODY", "The construction of the Bhor Ghat incline between 1856 and 1863 was one of the most perilous engineering undertakings in railway history. Chief Engineer James John Berkley and contractor Solomon Tredwell mobilized an army of over 42,000 Indian laborers across steep ravines and vertical cliffs."),
            ("BODY", "The line required the excavation of 25 tunnels through hard volcanic trap basalt, totaling over 3,900 yards, alongside eight massive stone viaducts spanning yawning gorges up to 140 feet deep. Over two million pounds of gunpowder were detonated to blast ledge tracks into the mountainside."),
            ("BODY", "Heavy monsoon rains triggered devastating landslides that washed away freshly laid embankments. In 1859 and 1860, severe outbreaks of cholera and dysentery swept through the construction camps, claiming the lives of thousands of workers, as well as contractor Solomon Tredwell within days of his arrival.")
        ],
        # Page 11: Chapter 3 (cont.) - Completion and Opening of the Incline
        [
            ("HEADER", "Chapter 3 (Continued): The Grand Opening of May 1863"),
            ("BODY", "Following the death of Solomon Tredwell, his widow Alice Tredwell courageously took over the massive contract, retaining the engineering staff and driving the project to completion. By late 1862, the permanent way across the reversing station and all 25 tunnels had been securely laid."),
            ("BODY", "On May 12, 1863, the Bhor Ghat incline was officially declared open for regular traffic by the Governor of Bombay, Sir Bartle Frere. The journey from Bombay to Pune, which previously required days of grueling travel by palanquin or bullock cart over mountain passes, was compressed into five hours by rail."),
            ("BODY", "The reversing station remained in continuous operational service for over sixty years until modern realignment tunnels were bored in the late 1920s, remaining a celebrated monument to Victorian civil engineering.")
        ],
        # Page 12: Chapter 4 - Birth of the Electric Telegraph (1839-1850)
        [
            ("HEADER", "Chapter 4: The Birth of the Electric Telegraph in India (1839-1850)"),
            ("BODY", "Concurrently with the dawn of railways, British India witnessed the introduction of electric telecommunications. The pioneer of Indian telegraphy was Dr. William Brooke O'Shaughnessy, an Irish-born physician, toxicologist, and Professor of Chemistry at the Medical College in Calcutta."),
            ("BODY", "In 1839, only two years after Cooke and Wheatstone patented the electric telegraph in England, Dr. O'Shaughnessy conducted private telegraphic experiments in the Botanical Gardens of Calcutta. Using a crude galvanic battery and insulated iron wire strung along trees and bamboo posts, he transmitted electrical impulses across a 21-mile circuit."),
            ("BODY", "O'Shaughnessy recognized that standard European telegraph methods would fail in tropical India due to torrential monsoon rains, roaming wildlife, dense jungle vegetation, and atmospheric electrical disturbances. He designed thick uninsulated iron rods supported by heavy sal-wood posts, utilizing the earth itself as a return circuit.")
        ],
        # Page 13: Chapter 4 (cont.) - The Diamond Harbour Cable & O'Shaughnessy
        [
            ("HEADER", "Chapter 4 (Continued): The Experimental Diamond Harbour Cable of 1851"),
            ("BODY", "In 1850, Lord Dalhousie authorized Dr. William Brooke O'Shaughnessy to construct an official experimental telegraph line connecting Calcutta with the maritime anchorage at Diamond Harbour, a distance of approximately 30 miles down the Hooghly River."),
            ("BODY", "According to the archival records in the text, the laying and installation of the experimental Diamond Harbour underwater telegraph cable in 1851 was personally supervised by Dr. William Brooke O'Shaughnessy. Crossing the broad, silty channel of the Hooghly River presented severe technical difficulties due to ferocious tidal bores and shifting mudbanks."),
            ("BODY", "To waterproof the submerged cable, Dr. O'Shaughnessy encased the conductor in layers of canvas saturated with pitch, melted beeswax, and gutta-percha. The submerged cable was successfully laid across the riverbed under his direct personal supervision in 1851, establishing an unbroken link between Diamond Harbour and the telegraph office in Calcutta."),
            ("BODY", "The line was an immediate operational triumph. It enabled shipping intelligence and naval arrivals at the Sandheads to be communicated to the Governor-General in Calcutta within minutes rather than taking several days by river cutter.")
        ],
        # Page 14: Chapter 4 (cont.) - Strategic Success and Sanction of the 4,000-Mile Wire
        [
            ("HEADER", "Chapter 4 (Continued): Approval of the Imperial Telegraph Scheme"),
            ("BODY", "The remarkable reliability of the Diamond Harbour experimental line convinced Lord Dalhousie of the transformative military and administrative potential of the electric wire. In February 1852, Dalhousie submitted an urgent minute to the Court of Directors in London urging the immediate construction of an all-India telegraph network."),
            ("BODY", "Dr. O'Shaughnessy sailed to London in 1852 to present his working models, technical reports, and cost estimates to the East India Company directors. He demonstrated that telegraph lines could be erected across India at a fraction of the cost incurred in Europe."),
            ("BODY", "The Court of Directors approved the scheme without delay, sanctioning the construction of a 4,000-mile network connecting Calcutta, Agra, Lahore, Bombay, and Madras. Dr. O'Shaughnessy was appointed the first Superintendent of Electric Telegraphs in India.")
        ],
        # Page 15: Chapter 5 - Lord Dalhousie's Railway Minute of 1853
        [
            ("HEADER", "Chapter 5: Lord Dalhousie's Railway Minute of 1853"),
            ("BODY", "On April 20, 1853 - four days after the opening of the Bombay-Tannah line - Governor-General Lord Dalhousie penned his landmark Comprehensive Railway Minute. This 100-page state paper formulated the strategic master plan for railway construction across the entire subcontinent."),
            ("BODY", "Dalhousie asserted that railways must not be constructed piecemeal to satisfy local mercantile interests, but along great trunk arteries connecting the four imperial presidencies: Calcutta, Bombay, Madras, and the northwestern frontier at Peshawar."),
            ("BODY", "He argued that a coordinated trunk network would multiply the military efficiency of the British army fourfold, permit the rapid concentration of forces against internal revolts or external aggression, integrate rural agricultural markets, and protect the empire against widespread regional famines.")
        ],
        # Page 16: Chapter 5 (cont.) - Standard Broad Gauge Selection
        [
            ("HEADER", "Chapter 5 (Continued): Adoption of the 5 ft 6 in Broad Gauge"),
            ("BODY", "A pivotal technical decision articulated in Dalhousie's 1853 Minute was the choice of track gauge. Warning against the 'battle of the gauges' that had crippled early British rail systems, Dalhousie rejected the standard English gauge of 4 feet 8.5 inches as inadequate for the expansive cargo and heavy cyclonic wind pressures of India."),
            ("BODY", "On the advice of Consulting Engineer W. Simms, Dalhousie decreed that all main trunk lines across British India must be built to a uniform broad gauge of 5 feet 6 inches (1,676 mm)."),
            ("BODY", "This broad gauge allowed for wider, more stable passenger carriages, heavier freight wagons, and larger fireboxes in steam locomotives, ensuring massive carrying capacity for agricultural staples and military baggage.")
        ],
        # Page 17: Chapter 6 - Great Indian Peninsula Railway Expansion
        [
            ("HEADER", "Chapter 6: GIPR Expansion Across the Deccan (1853-1865)"),
            ("BODY", "Following the completion of the line to Tannah, the Great Indian Peninsula Railway pushed inland. By 1854, track was laid through Salsette Island to Kalyan, where the iron line bifurcated into two great trunk routes."),
            ("BODY", "The South-Eastern trunk traversed the Bhor Ghat to reach Poona (Pune) in 1858 and pressed forward across the Deccan black-soil cotton tracts through Sholapur toward Raichur, where it was scheduled to link with the Madras Railway."),
            ("BODY", "The North-Eastern trunk advanced across the Konkan plain toward the Thul Ghat, aiming for Igatpuri, Bhusawal, and the rich cotton valleys of Khandesh and the Central Provinces, eventually meeting the East Indian Railway at Jubbulpore (Jabalpur).")
        ],
        # Page 18: Chapter 6 (cont.) - Bridging Estuaries and Creeks
        [
            ("HEADER", "Chapter 6 (Continued): Engineering Coastal Viaducts and Bridges"),
            ("BODY", "Expanding railways through coastal Bombay demanded unprecedented bridge engineering. The Thane Creek viaduct, constructed in 1854, was one of the earliest large-scale iron rail bridges erected across tidal saltwater in Asia."),
            ("BODY", "Engineers utilized cast-iron screw piles driven deep into marine silt to secure piers against strong tidal currents. Basalt masonry abutments were erected using stone quarried from neighboring hills."),
            ("BODY", "The completion of these coastal crossings opened uninterrupted rail transport between the deepwater harbor of Bombay and the interior cotton plantations, causing cotton exports to boom dramatically during the American Civil War.")
        ],
        # Page 19: Chapter 7 - The East Indian Railway: Howrah to the Coalfields
        [
            ("HEADER", "Chapter 7: The East Indian Railway - Howrah to Raneegunge (1854-1855)"),
            ("BODY", "In eastern India, the East Indian Railway Company under Chief Engineer George Turnbull was pushing westward from the Hooghly River. On August 15, 1854, the first passenger train in eastern India ran from Howrah to Hooghly, covering 24 miles."),
            ("BODY", "The line was rapidly extended through the alluvial plains of Bengal, reaching the rich coal deposits of Raneegunge (Raniganj) in February 1855, over a distance of 121 miles from Howrah."),
            ("BODY", "Access to the Raneegunge coalfields was of fundamental economic importance. Prior to this connection, Indian steam locomotives were forced to burn imported English coal shipped at exorbitant freight rates or rely on seasoned wood fuel. Cheap domestic coal now powered both locomotives and river steamboats.")
        ],
        # Page 20: Chapter 7 (cont.) - The Gangetic Trunk Line
        [
            ("HEADER", "Chapter 7 (Continued): Advancing up the Ganges Valley"),
            ("BODY", "From Raniganj, the East Indian Railway planned its grand trunk line following the ancient trade corridor along the southern bank of the Ganges. The alignment aimed to connect Patna, Benares (Varanasi), Allahabad, Kanpur (Cawnpore), and Agra, culminating at Delhi."),
            ("BODY", "The engineering challenge in the Gangetic plain was not mountain gradients, but river inundations. During the monsoon, rivers such as the Son, the Yamuna, and the Ganges swelled into miles-wide torrents, requiring immense masonry and iron bridges with foundations sunk up to 100 feet beneath the riverbeds."),
            ("BODY", "The Son River Bridge near Patna, completed in 1862, consisted of 28 spans of 150 feet each, ranking as the second longest bridge in the world at the time of its inauguration.")
        ],
        # Page 21: Chapter 8 - The Madras Railway and Southern Corridors
        [
            ("HEADER", "Chapter 8: The Madras Railway and Southern Corridors (1853-1860)"),
            ("BODY", "In the Madras Presidency, railway construction was chartered to the Madras Railway Company. The first line was surveyed from Royapuram (Madras) toward the military cantonment at Arcot (Wallajah Road), spanning 63 miles."),
            ("BODY", "Under Chief Engineer Major Jenkins, construction progressed through the dry red-soil plains of Tamil Nadu. The line was inaugurated for passenger traffic on July 1, 1856, marking the third major railway operational center in India."),
            ("BODY", "From Arcot, the Madras Railway expanded southwest toward the natural break in the Western Ghats known as the Palghat Gap. This strategic geographical gap allowed the iron road to reach the Malabar Coast at Beypore (Calicut) without scaling mountain heights.")
        ],
        # Page 22: Chapter 8 (cont.) - Branch Lines to Bangalore and Nagapattinam
        [
            ("HEADER", "Chapter 8 (Continued): The Mysore and Cauvery Branches"),
            ("BODY", "In 1864, a branch line from Jolarpettai ascended the Mysore plateau to reach Bangalore Cantonment, establishing rail connectivity for British garrisons and commercial planters in Mysore."),
            ("BODY", "Further south, the Great Southern of India Railway was chartered to build lines in the fertile Cauvery Delta. Opening in 1861 between Negapatam (Nagapattinam) and Trichinopoly (Tiruchirappalli), this railway carried enormous quantities of rice for export to Ceylon."),
            ("BODY", "These southern corridors differed from northern lines by carrying a predominance of agricultural commodities and pilgrim passenger traffic traveling to major temple complexes.")
        ],
        # Page 23: Chapter 9 - Transcontinental Telegraph Consolidation
        [
            ("HEADER", "Chapter 9: The Imperial Electric Telegraph Network (1852-1856)"),
            ("BODY", "Between 1853 and 1856, Dr. William Brooke O'Shaughnessy orchestrated an astonishing feat of rapid telecommunications engineering. In under three years, a workforce of military sappers and civilian laborers strung over 4,000 miles of electric telegraph wire across the Indian empire."),
            ("BODY", "The main telegraph trunk line linked Calcutta to Agra via the Grand Trunk Road, continuing onward to Delhi, Lahore, and Peshawar on the Afghan frontier. From Agra, a second trunk extended south through Gwalior and Indore to Bombay, while a third line connected Bombay with Madras."),
            ("BODY", "By March 1855, the telegraph was thrown open for private commercial and public messages, allowing merchants in Calcutta to exchange instantaneous commodity prices with brokers in Bombay.")
        ],
        # Page 24: Chapter 9 (cont.) - Technical Innovations in Tropical Telegraphy
        [
            ("HEADER", "Chapter 9 (Continued): Uninsulated Iron Rods and Bamboo Posts"),
            ("BODY", "O'Shaughnessy's success rested on bold technical adaptations to tropical environments. Rather than using fragile drawn copper wires that snapped easily, he employed thick ungalvanized iron rods weighing 1,200 pounds per mile, which were welded together on site."),
            ("BODY", "These thick rods resisted corrosion, lightning strikes, and the weight of swinging monkeys and birds of prey. In dense forest stretches where timber rotted rapidly, he utilized masonry pillars, cast-iron screw posts, and seasoned bamboo canes treated with boiling coal-tar."),
            ("BODY", "To cross wide untamed rivers, he suspended aerial wire spans up to 1,500 yards between towering wooden masts, or submerged heavy gutta-percha insulated cables anchored with lead weights in river silt.")
        ],
        # Page 25: Chapter 9 (cont.) - Organization of the Telegraph Department
        [
            ("HEADER", "Chapter 9 (Continued): Administrative Staffing and Training"),
            ("BODY", "To operate the extensive network, O'Shaughnessy established a formal Telegraph Department with headquarters in Calcutta. He recruited young soldiers from British regiments and educated Indian youths from the Thomason Engineering College at Roorkee and Presidency College at Calcutta."),
            ("BODY", "Operators were trained in Morse code transmission, battery maintenance using Daniell cells, and electrical fault detection. Signallers were stationed at remote outposts in the wilderness, enduring extreme heat, malaria, and isolation to keep the circuits operational 24 hours a day."),
            ("BODY", "By the end of 1856, the Indian telegraph system had transmitted over 200,000 official and private messages, operating at a tariff of 1 rupee per 16 words for every 400 miles.")
        ],
        # Page 26: Chapter 10 - The 1857 Uprising and Communications
        [
            ("HEADER", "Chapter 10: The Crisis of 1857 and Imperial Communications"),
            ("BODY", "In May 1857, the great rebellion against East India Company rule erupted at Meerut and Delhi. In this supreme political crisis, the newly built railway and telegraph networks played a decisive role in shaping military outcomes."),
            ("BODY", "While rebel sepoys recognized the strategic danger of the 'lightning wires' and cut thousands of miles of telegraph lines across the North-Western Provinces, signallers managed to transmit crucial warnings before stations were overrun."),
            ("BODY", "At Delhi on May 11, 1857, young telegraph operators Brendish and Pilkington remained at their keys until rebel troops entered the compound, dispatching the famous final message to Ambala and Lahore: 'The sepoys have come in from Meerut and are burning everything... we must close now.'")
        ],
        # Page 27: Chapter 10 (cont.) - The Telegraph That Saved India
        [
            ("HEADER", "Chapter 10 (Continued): Strategic Intelligence and Troop Deployment"),
            ("BODY", "The timely warning received at Lahore enabled Sir John Lawrence and Robert Montgomery to immediately disarm native regiments at Mian Mir before mutinies could organize, preserving the Punjab as a loyal base from which to recapture Delhi."),
            ("BODY", "Simultaneously, the railway between Calcutta and Raniganj expedited the movement of British reinforcements under Colonel James Neill toward Benares and Allahabad, bypassing the slow river navigation of the Ganges."),
            ("BODY", "As rebel leader Robert Montgomery later observed, and as historians frequently quote, 'The electric telegraph saved British India.' Without instantaneous communication between Calcutta and the Punjab, coordinated British military response would have been impossible.")
        ],
        # Page 28: Chapter 10 (cont.) - Post-1857 Crown Governance and Reorganization
        [
            ("HEADER", "Chapter 10 (Continued): The 1858 Government of India Act"),
            ("BODY", "Following the suppression of the 1857 revolt, the British Parliament passed the Government of India Act of 1858, dissolving the East India Company and transferring sovereign authority directly to the British Crown under Queen Victoria."),
            ("BODY", "The newly established India Office in London and the Public Works Department in Calcutta prioritized the rapid acceleration of both railway and telegraph networks as supreme instruments of military pacification and imperial defense."),
            ("BODY", "The Crown administration reaffirmed all existing contracts with private railway companies, continuing the 5% guarantee terms to ensure that foreign capital continued flowing into strategic transport lines without interruption.")
        ],
        # Page 29: Chapter 11 - The Thul Ghat Incline: Northern Ascent
        [
            ("HEADER", "Chapter 11: The Thul Ghat Incline - Conquering the Northern Sahyadris"),
            ("BODY", "While the Bhor Ghat connected Bombay with Pune and the south, the Thul Ghat (Thal Ghat) incline was engineered to carry the GIPR North-Eastern line across the Sahyadri barrier toward Khandesh and northern India."),
            ("BODY", "Ascending from Kasara to Igatpuri, the Thul Ghat incline climbed an elevation of 972 feet over a distance of 9.5 miles. Commenced in 1857 and completed in 1865, it was surveyed under Chief Engineer James John Berkley and executed by contractor Messrs. Wythes and Jackson."),
            ("BODY", "The engineering works rivaled the Bhor Ghat in audacity, comprising 13 tunnels, 6 viaducts, and an extensive reversing station layout designed to negotiate the jagged volcanic ridge of the northern escarpment.")
        ],
        # Page 30: Chapter 11 (cont.) - Comparative Engineering: Bhor vs Thul Ghat
        [
            ("HEADER", "Chapter 11 (Continued): Comparative Gradient Ratios and Structures"),
            ("BODY", "Archival comparisons in the Public Works reports highlight the technical differences between the two great mountain inclines of western India."),
            ("BODY", "While the Bhor Ghat featured a total vertical rise of 1,831 feet with a severe gradient ratio of 1 in 37 across its steepest section, the Thul Ghat rose 972 feet with a ruling gradient ratio of 1 in 56, incorporating a maximum slope of 1 in 37 on localized sections."),
            ("BODY", "Both passes made use of switchback reversing stations, where ascending trains entered a terminal siding to reverse direction, allowing locomotives to conquer precipitous terrain that defied direct continuous tracking.")
        ],
        # Page 31: Chapter 12 - Lord Lawrence and State Railways (1869-1880)
        [
            ("HEADER", "Chapter 12: Lord Lawrence and the State Railway Era (1869-1880)"),
            ("BODY", "By the late 1860s, the financial shortcomings of the Old Guarantee System had become glaringly apparent to colonial financial administrators. The guaranteed 5% annual interest paid to private companies had created a persistent drain on the Indian treasury, totaling over 12 million pounds sterling in net subsidies."),
            ("BODY", "In 1869, Viceroy Lord Lawrence issued an influential minute condemning the guarantee system. He demonstrated that private companies had built lines with excessive extravagance, costing an average of 18,000 pounds per mile, because they had no financial interest in keeping costs low."),
            ("BODY", "Lord Lawrence advocated that future railway construction be undertaken directly by the State through government engineers, financed by public debt raised directly in London at lower interest rates of 3.5 to 4 percent.")
        ],
        # Page 32: Chapter 12 (cont.) - The Metre Gauge Compromise
        [
            ("HEADER", "Chapter 12 (Continued): Introduction of the Metre Gauge (1870)"),
            ("BODY", "To reduce construction expenses for secondary and branch lines, the Government of India introduced the Metre Gauge (1,000 mm) in 1870 under Viceroy Lord Mayo."),
            ("BODY", "Lines such as the Rajputana-Malwa State Railway and the Northern Bengal State Railway were constructed in metre gauge at less than half the cost per mile of the original broad-gauge lines."),
            ("BODY", "While this dual-gauge policy accelerated network mileage into economically backward regions, it created an enduring technical problem: the 'break of gauge', which required time-consuming and expensive transshipment of freight and passengers at junction stations.")
        ],
        # Page 33: Chapter 13 - Indo-European Submarine Cables
        [
            ("HEADER", "Chapter 13: Indo-European Telegraph Linkages (1864-1870)"),
            ("BODY", "The strategic vulnerability of an isolated Indian telegraph network became intolerable to London after 1857. Efforts were immediately launched to connect India directly with Great Britain via overland and submarine cable routes."),
            ("BODY", "In 1864, the Government of India laid the Persian Gulf Submarine Cable from Karachi to Bushire and Fao under the supervision of Colonel Patrick Stewart and Sir Frederic Goldsmid. Connecting with Turkish and European landlines, this achieved the first telegraphic link between London and Calcutta."),
            ("BODY", "However, early messages took several days to traverse the fragmented Ottoman lines. In 1870, John Pender's Eastern Telegraph Company completed an all-submarine cable via Gibraltar, Malta, the Red Sea, and Aden to Bombay, reducing telegraphic transmission time between London and Bombay to under an hour.")
        ],
        # Page 34: Chapter 13 (cont.) - Impact on Global Trade and Imperial Rule
        [
            ("HEADER", "Chapter 13 (Continued): Financial Synchronization and Governance"),
            ("BODY", "The instant communication link via the Red Sea submarine cable revolutionized Indian commerce and governance. Commodity prices in Bombay, Calcutta, and Liverpool synchronized in real time."),
            ("BODY", "The Viceroy in Calcutta, who had previously exercised vast discretionary authority owing to the weeks-long delay of maritime mail dispatches, was brought under immediate telegraphic control from the Secretary of State for India in Whitehall."),
            ("BODY", "Merchants could now execute forward contracts, charter cargo steamships through the newly opened Suez Canal (1869), and adjust cotton and wheat purchasing orders with instantaneous telegraphic dispatches.")
        ],
        # Page 35: Chapter 14 - Famine Relief Commissions and Protective Lines
        [
            ("HEADER", "Chapter 14: Famines and Protective Railway Policies (1876-1885)"),
            ("BODY", "The devastating Great Famine of 1876-1878, which swept through Madras, Mysore, Hyderabad, and Bombay, resulted in millions of deaths and exposed catastrophic deficiencies in food grain distribution."),
            ("BODY", "The subsequent Famine Commission of 1880, presided over by General Sir Richard Strachey, concluded that British India urgently required at least 20,000 miles of railways to protect the population against starvation by enabling food grains to be moved swiftly from surplus to famine-stricken provinces."),
            ("BODY", "The Commission recommended the creation of a 'Famine Relief and Insurance Grant' of 1.5 million rupees annually, half of which was earmarked directly for the construction of 'protective railways' and irrigation works in drought-prone districts.")
        ],
        # Page 36: Chapter 14 (cont.) - Grain Markets and the Price Equalization Debate
        [
            ("HEADER", "Chapter 14 (Continued): The Contested Impact on Food Security"),
            ("BODY", "While the colonial administration praised railways as life-saving instruments that eradicated local famines of food, nationalist critics led by Romesh Chunder Dutt and Dadabhai Naoroji argued that the iron road intensified 'famines of purchasing power'."),
            ("BODY", "They observed that railways integrated rural markets so rapidly that grain was drained out of peasant granaries into export ports, equalizing food prices across the country at rates that starving landless laborers could not afford."),
            ("BODY", "Nevertheless, the Famine Commission's recommendations spurred an aggressive wave of construction, expanding the network from 9,000 miles in 1880 to nearly 16,000 miles by 1890.")
        ],
        # Page 37: Chapter 15 - Signaling and Operational Safety
        [
            ("HEADER", "Chapter 15: Signaling, Interlocking, and Safety Innovations (1870-1890)"),
            ("BODY", "As traffic density multiplied on single-track trunk lines, severe head-on collisions and derailments forced the adoption of rigorous mechanical safety standards across Indian railways."),
            ("BODY", "In the early years, trains were dispatched using the primitive 'time-interval system', relying on station guards and handwritten telegraph line-clear messages. Inevitable human errors led to tragic accidents, including the Bhor Ghat disaster of 1869."),
            ("BODY", "During the 1880s, the 'Absolute Block System' was made mandatory on all passenger routes. Neale's Ball Token Instrument was introduced, requiring locomotive drivers to carry a physical metal sphere extracted from an electrical token apparatus before entering a block section.")
        ],
        # Page 38: Chapter 15 (cont.) - Mechanical Interlocking and Continuous Brakes
        [
            ("HEADER", "Chapter 15 (Continued): Vacuum Brakes and Cabin Interlocking"),
            ("BODY", "Alongside electric token instruments, mechanical interlocking was introduced at major stations by engineers Saxby and Farmer. Interlocking levers prevented signals from showing 'clear' unless track points were mechanically set and locked in the correct alignment."),
            ("BODY", "Furthermore, the automatic continuous vacuum brake was gradually fitted to passenger rolling stock, replacing hand-operated screw brakes. This innovation drastically reduced stopping distances, enabling passenger express trains to operate safely at speeds up to 45 miles per hour.")
        ],
        # Page 39: Chapter 16 - Locomotive Workshops & Industrial Labor
        [
            ("HEADER", "Chapter 16: Locomotive Workshops and Industrial Labor"),
            ("BODY", "To maintain thousands of locomotives, carriages, and wagons, railway companies established gigantic industrial engineering workshops that became the earliest centers of modern factory labor in India."),
            ("BODY", "The East Indian Railway founded the sprawling Jamalpur Locomotive Workshops in Bihar in 1862, which grew into the largest industrial complex in South Asia, complete with iron foundries, rolling mills, and technical training institutes."),
            ("BODY", "In Bombay, the GIPR established the Parel Workshops in 1877, while the Bombay, Baroda & Central India Railway built its facilities at Lower Parel. In the south, the Madras Railway operated major workshops at Perambur.")
        ],
        # Page 40: Chapter 16 (cont.) - Labor Hierarchy and Apprenticeship
        [
            ("HEADER", "Chapter 16 (Continued): The Racial Division of Technical Labor"),
            ("BODY", "The social organization of railway workshops mirrored colonial racial hierarchies. Supervisory positions, locomotive engine drivers, and chief mechanics were strictly reserved for Europeans and Anglo-Indians, who received preferential housing, company schools, and higher wage scales."),
            ("BODY", "Indian artisans and laborers were relegated to lower-paid manual trades, working as firemen, boilermakers, track khalasis, and gangmen. Despite these barriers, Indian workers gradually mastered advanced metallurgy, lathe machining, and boilermaking, forming the vanguard of India's organized industrial working class.")
        ],
        # Page 41: Chapter 17 - Frontier Railways and Strategic Defense
        [
            ("HEADER", "Chapter 17: Frontier Railways and Strategic Defense (1880-1895)"),
            ("BODY", "During the late 19th century, imperial defense priorities shifted decisively toward the North-West Frontier due to fear of Russian expansionism in Central Asia ('The Great Game')."),
            ("BODY", "The Government of India amalgamated several pioneer lines into the unified North Western State Railway in 1886, undertaking the construction of costly strategic lines through desolate mountain passes with minimal commercial prospects."),
            ("BODY", "Lines were pushed through the treacherous Bolan Pass toward Quetta and Chaman on the border of Afghanistan, and along the Indus Valley to Rawalpindi, Peshawar, and the mouth of the Khyber Pass.")
        ],
        # Page 42: Chapter 17 (cont.) - Engineering the Bolan and Sind-Pishin Routes
        [
            ("HEADER", "Chapter 17 (Continued): Desert Heat and Mountain Torrents"),
            ("BODY", "Building the frontier railways through the Bolan and Sind-Pishin passes tested human endurance to the utmost. Engineers battled temperatures exceeding 125 degrees Fahrenheit in the desert of Sibi, followed by sub-zero blizzards in the upper mountain gorges."),
            ("BODY", "Flash floods routinely destroyed viaducts and carried away miles of newly laid track. The Chappar Rift bridge, where a steel span hung suspended between sheer mountain crags over a subterranean canyon, stood as a breathtaking monument to frontier military engineering.")
        ],
        # Page 43: Chapter 18 - Commercial Telegraphs & Tariff Reforms
        [
            ("HEADER", "Chapter 18: Postal Telegraphs and Tariff Democratization (1870-1895)"),
            ("BODY", "In 1870, the Indian Telegraph Department instituted sweeping administrative and tariff reforms to democratize access to the electric wire beyond high-ranking colonial officials and wealthy European merchants."),
            ("BODY", "Under Director-General D.G. Robinson, the telegraph was formally amalgamated with the Imperial Post Office in 1880, allowing combined post and telegraph offices to be opened in small mofussil towns and rural tahsil headquarters."),
            ("BODY", "A tiered tariff system was introduced, distinguishing between 'Urgent', 'Ordinary', and 'Deferred' telegrams. Press rates were slashed to a fraction of commercial rates, catalyzing the rapid growth of English and vernacular newspapers that received daily news wire dispatches.")
        ],
        # Page 44: Chapter 18 (cont.) - Linguistic Codes and Vernacular Messages
        [
            ("HEADER", "Chapter 18 (Continued): The Telegraph Peon and Vernacular Codes"),
            ("BODY", "To accommodate non-English communications, the Telegraph Department developed standardized transliteration codebooks for Hindustani, Bengali, Tamil, and Marathi, enabling vernacular messages to be transmitted via Latin Morse code."),
            ("BODY", "The khaki-clad telegraph peon on his bicycle, carrying the urgent red telegram envelope, became an iconic figure in Indian life, symbolizing momentous events - births, appointments, military postings, and sudden bereavements."),
            ("BODY", "By 1895, the Indian telegraph network spanned over 45,000 miles of wire and handled more than 4.5 million messages annually, serving as the neural network of subcontinental public life.")
        ],
        # Page 45: Chapter 19 - The Modified Guarantee Contracts of the 1880s
        [
            ("HEADER", "Chapter 19: The New Guarantee System (1880-1890)"),
            ("BODY", "By 1880, having exhausted direct state borrowing capacity during the famine crises, the Government of India reverted to private enterprise under a revised framework termed the 'Modified Guarantee System'."),
            ("BODY", "Under these new contracts, executed with companies like the Southern Mahratta Railway and the Bengal Nagpur Railway, the guaranteed interest rate was reduced from the original 5% to a lower rate of 3.5% or 4%."),
            ("BODY", "Crucially, the lines were declared state property from their inception, with the private companies acting merely as managing agents operating under strict government oversight, and the government retaining the right to terminate leases after 25 years.")
        ],
        # Page 46: Chapter 19 (cont.) - Consolidation and the Railway Board
        [
            ("HEADER", "Chapter 19 (Continued): Towards Unified Railway Administration"),
            ("BODY", "By the close of the 19th century, the Indian railway network exceeded 24,000 route miles, representing a colossal capital investment of over 300 million pounds sterling."),
            ("BODY", "The coexistence of state-managed lines, guaranteed company lines, and princely state railways (such as the Nizam's Guaranteed State Railway) created administrative fragmentation and divergent tariff policies."),
            ("BODY", "In 1901, Sir Thomas Robertson was appointed as Special Commissioner to investigate railway administration. His recommendations led to the creation of the centralized Railway Board in 1905, establishing unified managerial control over all Indian lines under the Department of Commerce and Industry.")
        ],
        # Page 47: Chapter 20 - Economic Transformation & Market Integration
        [
            ("HEADER", "Chapter 20: Economic Integration and Market Transformation"),
            ("BODY", "The economic consequences of five decades of railway and telegraph expansion were profound and multifaceted. The iron road dissolved centuries of geographic isolation, connecting landlocked agrarian hinterlands directly with international maritime ports."),
            ("BODY", "Regional price disparities for staple food grains - wheat, rice, pulses, and oilseeds - diminished drastically across India, creating a unified national commodity market. Cash-crop cultivation boomed as farmers shifted land from coarse grains to cotton, jute, tea, and sugarcane for export."),
            ("BODY", "At the same time, cheap British manufactured cotton textiles flooded rural markets via rail lines, accelerating the de-industrialization of traditional handloom weavers across Bengal, Awadh, and the Deccan.")
        ],
        # Page 48: Chapter 20 (cont.) - Historiographical Debates
        [
            ("HEADER", "Chapter 20 (Continued): Historiographical Perspectives"),
            ("BODY", "Modern historians remain divided over the balance sheet of colonial infrastructure in India. Imperial apologists celebrated railways and telegraphs as the supreme civilizing gift of British rule, uniting a fractured subcontinent under modern law and order."),
            ("BODY", "In contrast, nationalist and Marxist historians, such as Romesh Chunder Dutt and Daniel Thorner, emphasized the extractive character of colonial railways. Thorner characterized the guaranteed private companies as 'private enterprise at public risk', pointing out that lines were laid out primarily for imperial defense and raw material extraction rather than indigenous industrial development."),
            ("BODY", "Contemporary scholarship views the networks as dual-edged: tools of imperial control that simultaneously created the physical infrastructure, unified public sphere, and shared mobility upon which modern Indian national consciousness arose.")
        ],
        # Page 49: Archival Document Transcripts (1849-1855)
        [
            ("HEADER", "Archival Transcripts: Selected Despatches and Letters Patent"),
            ("BODY", "Transcript Document A-1849: Extract from the Indenture between the East India Company and the Great Indian Peninsula Railway Company, dated August 17, 1849:\n\n"
                     "'The said East India Company do hereby guarantee and agree to pay unto the said Railway Company interest at the rate of Five Pounds per centum per annum (5%) upon all such sums of money as shall be paid by the Railway Company into the Treasury of the said East India Company, such payment to be made half-yearly and to be chargeable upon the Revenues of India.'"),
            ("BODY", "Transcript Document B-1851: Extract from the Minutes of Consultations, Home Department (Electric Telegraph), Fort William, November 1, 1851:\n\n"
                     "'The Most Noble the Governor-General in Council records his highest approbation of the remarkable skill and personal energy displayed by Dr. William Brooke O'Shaughnessy in the successful completion of the experimental line to Diamond Harbour, including the submersion of the underwater cable across the Hooghly.'"),
            ("BODY", "Transcript Document C-1858: Dispatch from Chief Engineer J.J. Berkley regarding the Khandala Reversing Station:\n\n"
                     "'The sheer cliff barrier of the Bhor Ghat having precluded any direct forward track within safe adhesion, the reversing station has proved entirely efficacious in negotiating the ruling gradient of 1 in 37 without accident.'")
        ],
        # Page 50: Chronological Appendix (1845-1900)
        [
            ("HEADER", "Chronological Appendix: Chronology of Indian Railways and Telegraphs (1845-1900)"),
            ("BODY", "1845: Formation of East Indian Railway (EIR) and Great Indian Peninsula Railway (GIPR) in London.\n"
                     "1849: Contract terms executed granting private railway companies a 5% guaranteed annual interest rate.\n"
                     "1851: Dr. William Brooke O'Shaughnessy lays experimental Diamond Harbour underwater telegraph cable.\n"
                     "1853 (April 16): First commercial passenger railway opens from Bombay (Bori Bunder) to Tannah (21 miles).\n"
                     "1853 (April 20): Lord Dalhousie issues landmark Railway Minute proposing trunk network on 5 ft 6 in broad gauge.\n"
                     "1854 (August 15): First passenger train in eastern India runs between Howrah and Hooghly (24 miles).\n"
                     "1855: The 4,000-mile electric telegraph network opens for public traffic connecting Calcutta, Agra, Bombay, and Madras.\n"
                     "1856: Madras Railway opens line between Royapuram and Arcot (Wallajah Road).\n"
                     "1857: Telegraph warning from Delhi signallers enables timely defense during military uprising.\n"
                     "1863: Bhor Ghat incline and Khandala reversing station officially opened with 1 in 37 steepest gradient.\n"
                     "1865: Thul Ghat incline opened, connecting Bombay with the Central Provinces and northern India.\n"
                     "1869: Lord Lawrence introduces direct State Railway construction; eliminates Old Guarantee System.\n"
                     "1870: Submarine cable via Red Sea connects Bombay to London; Metre Gauge (1,000 mm) adopted for branch lines.\n"
                     "1880: Famine Commission recommends expansion to 20,000 miles; New Guarantee System initiated at 3.5%-4%.\n"
                     "1886: North Western State Railway unified for frontier military defense.\n"
                     "1895: Indian telegraph network surpasses 45,000 route miles; 4.5 million telegrams transmitted annually.\n"
                     "1900: Total railway route mileage reaches 24,750 miles, marking five decades of transformation."),
            ("BODY", "End of Archival Chronicle Folios. Certified authentic transcription from historical records.")
        ]
    ]

    for page_idx, elements in enumerate(pages_content, start=1):
        page = doc.new_page(width=612, height=792)  # Standard Letter size
        
        # Draw decorative border
        page.draw_rect(fitz.Rect(45, 45, 567, 747), color=(0.75, 0.8, 0.88), width=1)
        
        # Separate title/header elements and body elements
        header_text = ""
        title_text = ""
        subtitle_text = ""
        body_paras = []
        
        for elem_type, elem_text in elements:
            if elem_type == "TITLE":
                title_text = elem_text
            elif elem_type == "SUBTITLE":
                subtitle_text = elem_text
            elif elem_type == "HEADER":
                header_text = elem_text
            elif elem_type == "BODY":
                body_paras.append(elem_text)
                
        body_content = "\n\n".join(body_paras)
        
        if title_text:
            # Page 1: Title page
            insert_autofit(page, fitz.Rect(55, 65, 557, 105), title_text, max_fs=18, min_fs=14, fontname="hebo", color=(0.1, 0.2, 0.4), align=fitz.TEXT_ALIGN_CENTER)
            insert_autofit(page, fitz.Rect(55, 110, 557, 160), subtitle_text, max_fs=11, min_fs=9, fontname="heit", color=(0.3, 0.35, 0.4), align=fitz.TEXT_ALIGN_CENTER)
            page.draw_line(fitz.Point(55, 168), fitz.Point(557, 168), color=(0.1, 0.2, 0.4), width=1.5)
            
            # Body box
            insert_autofit(page, fitz.Rect(55, 185, 557, 715), body_content, max_fs=10.5, min_fs=8.5, fontname="helv", color=(0.15, 0.15, 0.2))
        else:
            # Chapter / Content page
            insert_autofit(page, fitz.Rect(55, 60, 557, 105), header_text, max_fs=12.5, min_fs=9.5, fontname="hebo", color=(0.1, 0.2, 0.4))
            page.draw_line(fitz.Point(55, 110), fitz.Point(557, 110), color=(0.7, 0.75, 0.82), width=1)
            
            # Body box
            insert_autofit(page, fitz.Rect(55, 120, 557, 715), body_content, max_fs=10.0, min_fs=8.0, fontname="helv", color=(0.15, 0.15, 0.2))

        # Draw footer line and page number
        page.draw_line(fitz.Point(55, 725), fitz.Point(557, 725), color=(0.75, 0.8, 0.88), width=0.8)
        footer_text = f"Folio / Page {page_idx} of 50 - Modern History & Archival Chronicle Assistant (Indian Railways & Telegraphs)"
        page.insert_text(fitz.Point(55, 737), footer_text, fontsize=8, fontname="heit", color=(0.45, 0.5, 0.55))

    doc.save(filename)
    doc.close()
    print(f"Successfully generated 50-page PDF at: {filename}")

if __name__ == "__main__":
    build_pdf()
