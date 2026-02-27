# Tokenised Multi-client Provisioning for Dynamic Searchable Encryption with Forward and Backward Privacy

## 文档信息
- 来源 PDF: `/Users/cyan/code/paper/ref-thesis/Bag 等 - 2024 - Tokenised Multi-client Provisioning for Dynamic Searchable Encryption with Forward and Backward Priv.pdf`
- DOI: `10.1145/3634737.3657018`
- 转换时间: `2026-02-13 21:59:28`
- 说明: 自动抽取得到的 Markdown，可能存在少量断词和双栏排版残留。

---

## 正文（自动抽取）

TokenisedMulti-client Provisioning for Dynamic Searchable
EncryptionwithForwardandBackwardPrivacy
ArnabBag Sikhar Patranabis DebdeepMukhopadhyay
Indian Institute of Technology IBMResearchIndia Indian Institute of Technology
Kharagpur Bengaluru, India Kharagpur
Kharagpur, India Kharagpur, India
ABSTRACT ACMReferenceFormat:
Searchable Symmetric Encryption (SSE) has opened up an attrac- ArnabBag,SikharPatranabis,andDebdeepMukhopadhyay.2024.Tokenised
tive avenue for privacy-preserved processing of outsourced data Multi-client Provisioning for Dynamic Searchable Encryption with Forward
ontheuntrusted cloud infrastructure. SSE aims to support efÏcient andBackwardPrivacy.InACMAsiaConferenceonComputerandCommuni-
Booleanqueryprocessingwithoptimalstorageandsearchoverhead cations Security (ASIA CCS ’24), July 1–5, 2024, Singapore, Singapore. ACM,
over large real databases. However, current constructions in the NewYork,NY,USA,17pages.https://doi.org/10.1145/3634737.3657018
literature lack the support for multi-client search and dynamic up- 1 INTRODUCTION
dates to the encrypted databases, which are essential requirements
for the widespread deployment of SSE on real cloud infrastructures. Recent advancements in cloud computing have fuelled the devel-
Triviallyextendingastate-of-the-artsingleclientdynamicconstruc- opmentofprivacy-preserved processing of sensitive data on thirdtion, such as ODXT (Patranabis et al., NDSS’21), incurs significant party cloud servers. Outsourced processing and storing of users’
leakage that renders such extension insecure in practice. Currently, data are becoming standard practices for individuals and organisano SSE construction in the literature offers efÏcient multi-client tions. Presently, cloud infrastructures are responsible for handling
query processing and search with dynamic updates over large real users’ private data obtained from devices/systems used by ordinary
databases while maintaining a benign leakage profile. citizens, government and industrial establishments. For extended
This work presents the first dynamic multi-client SSE scheme functionalities, the cloud service providers often delegate access
NomossupportingefÏcientmulti-clientconjunctiveBooleanqueries to users’ data to third-party entities. The involvement of the cloud
over an encrypted database. Precisely, Nomos is a multi-reader- service providers and other third-party entities - all of whom are
single-writer construction that allows only the gate-keeper (or the considered untrusted, raises deep concern about users’ data condata-owner) - a trusted entity in the Nomos framework, to update fidentiality and information privacy. Furthermore, modern cloud
the encrypted database stored on the adversarial server. Nomos applications serve multiple clients, and the data stored on the cloud
achievesforwardandtype-IIbackwardprivacyofdynamicSSEcon- is frequently updated. In this context, straightforward encryption
structions while incurring lesser leakage than the trivial extension thatprovideshighconfidentialityofdatatriviallylosestheabilityto
of ODXTtoamulti-client setting. Furthermore, our construction processinformationintheencryptedform,defeatingtheadvantage
is practically efÏcient and scalable - attaining linear encrypted stor- of using the cloud.
age and sublinear search overhead for conjunctive Boolean queries. Several elegant cryptographic primitives such as Fully Homo-
Weprovide an experimental evaluation of software implementa- morphic Encryption (FHE) [17, 18], Functional Encryption (FE) [4],
tion over an extensive real dataset containing millions of records. Oblivious RAM (ORAM) [20, 21] and Private Information Retrieval
The results show that Nomos performance is comparable to the (PIR) [2, 13, 29] allow implementing diverse functionalities over
state-of-the-art static conjunctive SSE schemes in practice. encrypted outsourced data. However, all of these approaches either
incur prohibitively heavy computation/storage overhead or require
CCSCONCEPTS extremely high communication bandwidth for real applications.
• Security and privacy → Cryptography; Management and In contrast, SSE offers theoretically robust and implementationqueryingofencrypteddata. efÏcient constructions for encrypted data processing, especially
searching, while leaking only benign information to untrusted
KEYWORDS parties. The benign leakage in SSE is formally quantified using
Searchable encryption, Dynamic, Multi-client precise leakage functions that capture the information leaked. We
elaborate more on the general SSE setting and construction below.
Permission to make digital or hard copies of all or part of this work for personal or 1.1 Searchable SymmetricEncryption
classroom use is granted without fee provided that copies are not made or distributed Searchable Symmetric Encryption (SSE) [6–12, 14–16, 19, 24–27,
for profit or commercial advantage and that copies bear this notice and the full citation
onthefirst page. Copyrights for components of this work owned by others than the 30, 32] allows querying an encrypted database privately without
author(s) must be honored. Abstracting with credit is permitted. To copy otherwise, or decryption. In contrast to the abovementioned approaches, SSE
republish,topostonserversortoredistributetolists,requirespriorspecificpermission
and/or a fee. Request permissions from permissions@acm.org. offers efÏcient and low-bandwidth constructions for encrypted
©2024Copyrightheldbytheowner/author(s). Publication rights licensed to ACM. information to untrusted parties. Fundamentally, an SSE scheme
ACMISBN979-8-4007-0482-6/24/07
https://doi.org/10.1145/3634737.3657018 offers the following capabilities.
• Allow an (or many) entity (potentially untrusted client) to efÏ- Is there a dynamic MRSW/MRMW SSE scheme with strong forward
ciently search encrypted queries over an encrypted database stored and backward privacy, linear storage requirements and sublinear
onthecloud(untrusted) without revealing the result to the server. search overheads – all collectively?
• Minimise the leakage during query (or update) such that the Asit turns out, the answer is no. ODXT supports dynamic upuntrusted entities receive only benign information. dates and conjunctive queries with sublinear search overhead and
Typical benign leakages include crude statistical information linear encryptedstorage.However,itisanSRSWconstructionwithrelated to the database elements, the query, or the result of the out support for multiple clients. Furthermore, ODXT is vulnerable
query - but do not include the actual associated (encrypted) data. to a particular leakage originating from the cross-terms in a con-
Thedatabase size, query pattern (the set of queries corresponding junctive query (discussed later) that can lead to complete query
to the same keyword), and the access pattern (the set of database recovery. Trivially extending ODXT to the multi-client setting by
records matching a given query) are a few such leakages typically delegating the search token generation phase from multiple clients
studied in the context of SSE. We present formal syntax of SSE (assumed to be semi-honest) to the data-owner (a trusted party)
with elaborate details in Section 2, and elaborate the study of these retains this leakage. We outline an attack process based on this leakleakages in the full version of the paper1 due lack of space. age in Section 3 that leads to complete recovery of the cross-terms.
DynamicSSE.AdynamicSSEconstruction[6–8,11,15,25,26]al- In brief, the existing SSE literature lacks dynamic SSE schemes in
lowsdynamicupdates(addingordeletingrecords)totheencrypted MRSWandMRMWsettings,whichhindersthewidespreadadopdatabase ofÒoaded to the cloud by the client. In contrast, static con- tion of SSE in encrypted processing tasks on the cloud.
structions do not allow updates to the database once it is encrypted. Thisworkaimstobridgethisgapbetweensecureandpractically
Theupdatecapability of dynamic constructions implies two secu- efÏcient SSE constructions and real multi-client cloud applications.
rity notions - forward privacy andbackward privacy.Informally,the Wesummariseourgoalswiththefollowingquestion.
forward privacy notion states that a current search operation can CanwedesignanefÏcient dynamic SSE scheme with forward and
not be linked to a future update operation, and backward privacy backward privacy in the MRSW setting?
dictates that an insertion operation followed by a deletion does Weshowinthispaperthatitispossibletodesignsuchascheme,
not reveal any information in a future search operation. These two and we present Nomos construction that achieves the aforemennotions are essential for dynamic schemes to prevent a certain class tionedpracticaldesignandsecuritygoals.Thefollowingsubsection
of attacks, specifically, the file injection attack [34]. lists the primary contributions of this work. We emphasise that
Multi-clientSSE.Amulti-clientSSEschemeallowsmultipleclients Nomos is a dynamic multi-keyword construction in the MRSW
to search (or update) the encrypted database. SSE schemes can be setting with forward and type-II backward privacy [7], which is a
classified in the following way according to the different entities stepping stone towards building “ideal” MRMW SSE constructions.
involved in the setting. Extending Nomos to the MRMW setting is of independent inter-
Single-Reader–Single-Writer (SRSW): Single-reader–single-writer est requiring separate in-depth exploration, and we leave this as a
or SRSWsetting has a single client and an untrusted cloud server. future work.
Thesingle client also acts as the data owner who has permission to 1.2 OurContributions
updatetheencrypteddatabaseontheserver.SRSWconstructions[8,
9, 11, 12, 14, 16, 19, 24–27, 32] have been extensively studied in the We summarise our main contributions of this work with brief
literature. A number of dynamic SRSWschemes[6–8,11,15,25,26] overview below.
have been proposed in recent years and ODXT by Patranabis et 1 Multi-client SSE. We present the first multi-client dynamial. [30]istheonlystate-of-the-artdynamicschemewithconjunctive cally updatable SSE construction Nomos for outsourced encrypted
query support. databases. Nomos supports efÏcient multi-keyword conjunctive
Multi-Reader–Single-Writer (MRSW): In the multi-reader–single- Boolean queries in the MRSW setting, which is essential for practiwriter or MRSW setting, multiple clients can interact with the cal cloud applications. To the best of our knowledge, this is the first
untrusted server to search (with individual trapdoors), and a single schemeintheliterature that can process conjunctive queries from
data owner can generate or update the encrypted database on the multiple clients with dynamic updates. Clients in Nomos obtain
untrusted server. search tokens from a trusted entity called gate-keeper, which is
Multi-Reader–Multi-Writer (MRMW): Multi-reader-multi-reader or allowed to update the encrypted database and holds the keys for
MRMWisthemost generic setting allowing multiple clients to token generation. The clients use the search tokens obtained from
search and update the encrypted database on the cloud server. gate-keeper to query over the encrypted database on the cloud
Ideally, cloud applications require multi-client access and dy- server. We use Oblivious Pseudo-random Function (OPRF)-based
namicupdatecapabilitytocatertoapplicationsoverdiversedatabases mechanismtodelegate the search token generation process to the
involving a potentially large number of users (or clients). Unfortu- gate-keeper; thus bypassing the need to share the secret keys for
nately, the literature on practically efÏcient MRSW and MRMWSSE token generation among multiple potentially semi-honest clients.
schemesissparseandentirely restricted to the static setting [5, 23], 2 Leakagemitigation. The Nomos construction mitigates a parwhichpromptsustoraisethefollowing question. ticular leakage originating from the cross-terms of conjunctive
queries. This leakage is inherently present in the state-of-the-art
1https://eprint.iacr.org/2024/573 ODXTscheme,andwediscussanattackflowthatshowsthatthe
Tokenised Multi-client Provisioning for Dynamic Searchable Encryption with Forward and Backward Privacy ASIACCS’24,July1–5,2024, Singapore, Singapore
trivial extension of ODXT to the multi-client setting remains vul- the experimental results and related discussion are provided in
nerable to this leakage that potentially breaks the scheme. Nomos Section 5, and we end with a concluding remark on our work. We
avoids this specific cross-term–based leakage exploitable from XSet have diverted the formal security analysis to the full version of the
accesses by introducing decorrelated XSet access pattern. We use paper1 due to lack of space.
a variant of Bloom Filter (BF), denoted as the Redundant Bloom
Filter (RBF), for decorrelating the repeated memory accesses (for 2 BASICNOTATIONSANDSYNTAX
XSet implemented using RBF) to mitigate the cross-term leakage. Weprovidethebasic notations and syntax of SSE below, which we
Using RBF has a minimal impact on the storage, communication follow throughout this paper. For ease of exposition, we assume
and computation overhead of Nomos compared to non-BF and the database to be a document collection indexed by keywords and
plain BF versions of our construction. uniquedocumentidentifiers.Moreprecisely,weassumeaninverted
3 Tokenisedsearch.Nomosallowseachclienttoobtainsearch index of keywords and corresponding document identifiers for a
tokens from the gate-keeper (the data owner holding the keys for documentcollection is available as the plain database.
token generation) individually and engage in the search protocol
with the server to retrieve the query result. The token generation 2.1 Basic Notations
processandsearchphaseworkasynchronously,althoughthesearch Data. We use w to represent a keyword and id to represent a docuphase requires the tokens to be generated first through the token mentidentifier in a database. We use Δ to denote the dictionary of
generation protocol. This tokenised search process for multiple all ws in a database and is number of ws in Δ. We represent the
clients allows us to avoid a three-party search protocol involving plain database as DB, and DB() represents the set of ids satisfying
a client, the gate-keeper, and the server, without blocking other a conjunctive query over DB. Similarly, for a single w, DB(w)
clients from invoking the token generation or the search protocol is the set of ids where w appears. The number of ids in DB() is
(whichever is available). This is a desirable capability in multi-user represented as |DB()|. For two values (or strings) and , ||
cloud applications where requests arrive asynchronously, and the 1 2 1 2
gate-keeper/cloud needs to serve as early as possible, reducing represents the concatenation of 1 and 2. The cardinality of a set
waiting time (for example, assigning doctors appointments based is denoted by ||, and for a string (or vector), || represents
onpatient details in medical applications). It can be easily adopted the length of . We represent the sequence , + 1,..., − 1,
into general cloud search applications where strong access control using [,] and 1,2,. . ., using []. Sampling a value from a
$
is necessary, such as ofÏce employee records and bank operations, distribution is expressed as ←− . We denote a negligible functo name a few. The tokenised functionality allows fine-grained tion as negl(). We denote the attribute of a w using (w), which is
user management and enforcing access permissions for each user essentially encoded as an index. More precisely, can be considered
individually in a multi-client setting. as a list of (w,) pairs, where (w) returns the attribute , where
4 Security analysis and implementation. We provide a con- w ∈ Δ and is a valid keyword attribute. We represent a set of
crete security analysis of Nomos using hybrid arguments of indis- valid keyword attribute combinations using P, from all unique
tinguishabilityframework.Nomossettingassumesthatgate-keeper keyword attributes for all ws in Δ. We denote the number of all
(or the data owner) is a trusted entity, and the cloud server is an unique keyword attributes using . We also assume that during
honest-but-curious polynomial-time adversarial entity. The clients an update, a complete document (containing multiple keywords)
are assumed to be semi-honest entities individually; that is, a semi- is replaced, and in this process, the existing records are deleted
honest client follows the specified token generation and search and added again with the modified content. In that case, update
protocol but can obtain/share additional information regarding the operations are usually done in batches of deletions followed by
queries issued or the tokens received. We provide an overview of additions of multiple (w,id) pairs.
the Nomosleakageprofile and concrete security analysis in the full Entities. We use C to represent a client and C = {C ,...,C }
version of the paper1 due to lack of space. 1
Weimplemented the Nomos framework using C++ (natively to represent a set of clients. We represent a data-owner by the
multi-threaded) with Redis2 as the database back-end. We used symbolD.WedenotetheserverusingS andthegate-keeperusing
the Enron dataset3 to evaluate Nomos performance, and we re- G(explained in Section 4). In a single client setting, D and G serve
port the results in Section 5. The experimental results show that thesamepurpose,andweusetheD symbolinthecontextofsingle
Nomosachieves linear storage overhead and sublinear search time, client constructions. However, in an MRSW multi-client setting, G
comparable to other state-of-the-art conjunctive SSE constructions. has the additional responsibility of generating search tokens for Cs.
Thus, we denote the single entity responsible for database update
WeprovidepreliminarynotationsandsyntaxinSection2,which in SRSWconstructions, such as OXT, ODXT, by D, and we denote
we follow throughout the manuscript. We present an attack in the single entity responsible for database update and search token
Section 3 on the trivial extension of ODXT to the multi-client generation for other clients, as in MC-ODXT or Nomos, by G. We
setting to demonstrate the devastating effect of cross-term leakage denote a polynomial-time adversary by A and a simulator using
onamulti-clientSSEconstruction.Weoutlinetherequiredsecurity SIM.
notions and challenges of designing multi-client SSE in Section 3.3.
We present our main Nomos construction in Section 4. Finally, 2.2 CryptographicPrimitives
2https://redis.io/ Wedenoteapseudo-randomfunction(PRF)by(,·) andaspecific
3https://www.cs.cmu.edu/~enron versionmappingtoF as (,·).Werepresentacollision-resistant

hash function as CRHF or with the symbol H, which we assume • SSE.GenToken(,sk). The GenToken routine is executed by a
can be modelled as a random oracle. Additionally, we use an au- client C ∈ C and G, where C ’s input is a query, and G’s input

thenticated encryption (AE) [3, 31] scheme with the routines AE = is the secret key sk, and at the end of execution, C receives the
{AE.Enc,AE.Dec} that is IND-CPA and and strongly UF-CMA-secure search token tk.
(unforgeability guarantee) [3]. • SSE.Search(tk;EDB). In this protocol, a client C sends the

Decisional DifÏe-Hellman assumption. Let G be a cyclic group search token tk obtained from G using GenToken method to S,
of prime order, and let be any uniformly sampled generator for andSlooksupEDBtoreturnthesetofmatchedencryptedrecords
G. The decisional DifÏe-Hellman (DDH) assumption is that for all R toC .
PPTalgorithms A, we have,

AnSSEschemeissaidtobecorrectiftheSSE.Searchroutine

·
≤ negl(), returns all the matching encrypted ids from EDB for a query.
Pr[A(, , , ) = 1] − Pr[A(, , , ) = 1]

$
SecurityofMRSWSSE.AdynamicMRSWSSEschemeSSEasde-
∗ scribedaboveissaidtobesecureifitfollowsthesecurityproperties
where,, ←− Z .
stated below.
Oblivious pseudo-randomfunction.Oblivious Pseudo-random Security against a semi-honest client. The following leakage function
Function (OPRF) is a cryptographic primitive that allows two par- parameterises the security of a dynamic MRSW SSE construction
ties to jointly evaluate a PRF where party A provides the input against a semi-honest client.
plaintext and party B inputs the key . At the end of the protocol, Setup Update GenToken Search
Areceives the output, which is indistinguishable from a regular LC = {LC , LC , LC , LC }
PRFevaluationwiththesame and,andpartyBreceivesnothing In this ensemble, LSetup encapsulates the leakage to a semi-
(or error/nothing symbol ⊥). C Update
Hashed DifÏe-Hellman OPRF. We use a specific instance of OPRF honest client during Setup, LC encapsulates the leakage to
a semi-honest client during Update, LGenToken encapsulates the
called hashed DifÏe-Hellman (DH) OPRF that works as follows - C Search
party A provides input and a randomly sampled value. A uses a leakage to a semi-honest client during GenToken, and LC
hash function which hashes an input to a group element of G. A encapsulates the leakage to a semi-honest client during Search.
uses to obtain () ∈ G and raises () to generate = (). AdynamicMRSWSSEschemeΠissaidtobesecureagainsta
Asends to B, and B raises by power to obtain = . B semi-honest PPT adversary A, who is allowed make = poly()
sends back to A, and A outputs = −1. We represent this OPRF queries, with respect to LC, there exists a polynomial time simulaevaluationas = OPRF(,).DH-OPRFisusedasacoreprimitive tor SIM, such that
inourconstructiontoallowmulti-clientsearch.Pleaserefer[28]for |Pr[RealΠ () = 1] − Pr[IdealΠ () = 1]| ≤ negl()
moredetailsonDH-OPRF4.NotethatthemainNomosconstruction A A,SIM
whereRealΠ andIdealΠ are defined in Algorithm 1 and 2 of
can be instantiated with a generic OPRF. We opted for DH-OPRF A A,SIM
for the ease of analytical exposition and implementation. in Appendix A, respectively.
Securityagainstasemi-honestserver.Thefollowingleakagefunction
### 2.3 SSESyntaxandSecurityDefinition parameterises the security of a dynamic MRSW SSE construction
WedenoteanSSEalgorithmsimplyusingSSE.WeuseEDBtode- against a semi-honest server.
L ={LSetup,LUpdate,LGenToken,LSearch}
notetheencrypteddatabasestoredontheencryptedserver.Weuse S S S S S
R todenotethesetofencrypted records returned upon searching Setup
In this ensemble, LS encapsulates the leakage to a semia conjunctive query - compactly expressed as R = EDB(). We
honest server during Setup, LUpdate encapsulates the leakage to
denote a conjunctive query as = w ∧ ... ∧ w where w ∈ Δ. S
1 a semi-honest server during Update, LGenToken encapsulates the
Without loss of generality, we assume w in has the least fre- S
1 leakage to a semi-honest server during GenToken, and LSearch
quency of updates. We call w as the special-term or s-term, and
1 S
w ,...,w are denoted as the cross-terms or x-terms. encapsulates the leakage to a semi-honest server during Search.
2 AdynamicMRSWSSEschemeΠissaidtobesecureagainsta
AdynamicMRSWSSEschemeSSEwithtokenisedmulti-client
search is defined by the following ensemble of algorithms. semi-honest PPT adversary A, who is allowed make = poly()
queries, with respect to L , there exists a polynomial time simula-
• SSE.Setup(1 ). This is a PPT algorithm run by G (who is the tor SIM, such that S
data-owner) that samples the master security key sk, the AE key
, and initialises the encrypted database EDB. Π Π
| [RealA() = 1] − [IdealA,SIM() = 1]| ≤ negl()
• SSE.Update(sk,{op,(w,id)};EDB). This is a PPT algorithm whereRealΠ andIdealΠ are defined in Algorithm 3 and 4 in
jointly executed by G and S, where G’s input is secret key sk, the A A,SIM
update record (w,id) and the type of the update op = {add,del}, Appendix A, respectively.
and Ss input is EDB. At the end of the protocol, EDB stored on S SSEdatastructures. SSE constructions heavily rely on the underis updated with the new record. lying data structures to store and efÏciently search over encrypted
data. We consider two widely used SSE-specific data structures in
4The constructions in this manuscript can be instantiated with a general syntax this work, namely TSet and XSet. We assume that EDB comprises
of OPRF. We opt for the specific instance of DH-OPRF for the ease of exposition with of both TSet and XSet (as required by the construction discussed
the existing construction structure of ODXT [30] and OSPIR-OXT [23]. later in Section 3 and 4).
Tokenised Multi-client Provisioning for Dynamic Searchable Encryption with Forward and Backward Privacy ASIACCS’24,July1–5,2024, Singapore, Singapore
TSet. TSet is an encrypted variant of a multi-map data structure that and querying the server S using those search tokens. Note that, in
stores the encrypted database in a structured form. Fundamentally, this MRSWsetting, we use the G notation instead D as it has the
TSetstoresandaccessesdataelementsinauniformlyindistinguish- additional responsibility of generating Cs search tokens.
able manner that hides the association of an w with respective ids. MC-ODXTworkflow. MC-ODXT follows the ODXT structure
Atahighlevel, TSet follows the typical syntax of a multi-map. withtheSetup,Update,Searchroutinesandanadditionalroutine
• Insertion: TSet[key] = val GenTokenforquerytokengeneration. The Setup routine sets up
• Retrieval: val = TSet[key] and initialises the parameters, data structures and generates the
TheTSetkeysaregenerated through PRFs (and SKE) such that the secret keys. If there is an initial DB present, G repeatedly invokes
probability of an A distinguishing two different ws from randomly Update on DB entries to update EDB stored on S. The Update
accessed (key,val) pairs is negligible. algorithm generates a unique TSet address addr for each (w,id) pair
XSet. XSet is a data structure typically used in multi-keyword SSE by appending a counter value with w and evaluating the resultschemes to support conjunctive queries (especially in the cross-tag ing value through a PRF. Since this counter value is incremented
family of constructions [9, 27, 30]). XSet stores the cross-term– with each update, an addr is never repeated (in other words, a
specific information that is used during conjunctive query search. unique addr is obtained in each update invocation). Furthermore,
Note that XSet does not store any encrypted information of in- the update routine treats an ADD or DEL op identically, as there is
dividual ws or ids; rather, it stores flags or bits associated with noconditional execution based on ADD or DEL. S stores the encross-terms that are generated using CRHF or PRFs. At a high level, crypted id in TSet (which is a part of EDB) along with a w-specific
an XSet has the following syntax, deblinding token (, this is required during search) received from
• Insertion: XSet[index] = , ∈ {0,1} G. Additionally, G generates an xtag (or cross-tag) by combining
• Retrieval: = XSet[index] wwithid(concatenated with op) through PRF and raising to the
power of (such that during a search, xtag can be recomputed
wheretheindex is typically generated from a combined input of w obliviously using the query tokens and ). G sends xtag to the
andidtoaCRHF,and = 1indicatesthat(w,id)isvalidpair(thatis server, and the server sets a bit 1 at address xtag in XSet.
wappearsindocumentid).Fordetailed properties and analysis of Prior to interacting with S in the Search, a C obtains a blinded
TSet and XSet, please refer [9]. We use a slightly different variant search token from G for a conjunctive query comprising of two
of TSet, as adopted in ODXT [30]. components. The first one constitutes of strap (or trapdoor corre-
WechooseODXTasourbaseconstructionfordevelopingthe sponding to the s-term) and bstags (or blinded search tags for TSet
look-up) corresponding to the s-term w . The second component
multi-client solution as ODXT is the only state-of-the-art dynamic 1
schemewithanefÏcient update and conjunctive query search. Un- consists of bxtraps (or blinded trapdoors for x-terms) corresponding to the x-terms w ,...,w . C sends these tokens to S to look
fortunately, ODXT itself does not support multi-client search. We 2
first transform ODXT into a multi-client construction MC-ODXT up EDB. In this process, S retrieves the encrypted ids using the
(see AppendixB)following[23].However,weshowthatMC-ODXT de-blinded bstags. It also computes the deblinded xtags for each
is vulnerable to cross-term leakage, and the following attack ex- x-term and retrieved encrypted id (concatenated with op) pair. S
ploits this leakage to break the scheme. checks whether the xtags for all cross terms and a particular id is
set to 1 in XSet. If all xtag locations are set, it returns the encrypted
3 ATTACKONMULTI-CLIENTSSE id (concatenated with op) to C. C locally checks if the id has been
EXPLOITINGCROSS-TERMLEAKAGE added for all ws in , and not deleted even for one w of . If it is
Weoutline an attack on the trivial multi-client extension of ODXT present for all ws, it keeps the id in the final result set, otherwise
(or MC-ODXT)following the approach in [23]. This attack demon- discards it.
strates that the presence of the same cross-terms across different Note that the xtag computation process is deterministic as it
queries leads to severe leakage through XSet access pattern, which refers to a physical location of a value in the memory (or storage).
can completely break MC-ODXT. More precisely, we show that a For validating a (w,id) pair, the same xtag address needs to be gensemi-honest C colluding with the semi-honest S can exactly re- erated each time the Search protocol encounters the same (w,id)
cover the query keywords of a legitimate C. Provided that enough pair. This association is revealed even across different queries havquery instances, the colluding C-S pair can recover the entire ing the same keyword issued by multiple clients and leads to the
keyworddictionary. This glaring vulnerability puts MC-ODXT (or leakage across multiple clients. The following example expounds
anyconstruction following the same approach) at risk of a severe onthis observation for a clearer understanding.
data leak. Our main construction Nomos adopts a computationally Table 1: An example of SSE execution sequence.
“lightweight” redundancy-based approach to reduce this leakage
while incurring minimal extra storage overhead without affecting Entity Time Operation Query/Data
C T1 Search w ∧w ∧w
the performance. 1 1 2 3
G T2 Update (w ,id)
Webriefly summarise the workflow of MC-ODXT algorithms 3
C T3 Search w ∧w
1 1 3
C T4 Search w ∧w
presented in Appendix B to identify the source of the leakage and 2 2 3
subsequently discuss the attack exploiting this leakage. The MC-
ODXTworkflowbelowinvolvesaclientC obtainingasearchtoken Consider the sequence of MC-ODXT events shown in Table 1.
for a conjunctive query = w ∧ ... ∧ w from the data owner G Assumethatw wasnotpresentinEDBduringT1.Itisinserted
1 3
into EDB at T2 by G, and queried again (as an x-term) at T3 by C Algorithm 1 Query recovery attack MC-ODXT in presence of
1 colluding semi-honest client and semi-honest server
followed by C at T4. Observe that these three instances of queries
2
andupdateinvolvew .Thesecondandthirdinstancesgeneratethe
## 3 Input: Query tokens (tks) and ws from semi-honest C , query tokens of
samextagfor (w ,id) pair following the MC-ODXT construction. benign C
3
Since S is assumed to be semi-honest, it can “see” that the same Output: W:thesetofcross-termwspresentin C ’s query
xtag is accessed in these instances. S’s ability to observe these 1: function CrossAttack
distinct accesses for xtags is the base of this attack below.
This two-phase attack assumes a semi-honest C that colludes 2: Build Phase
Server
with S in the attack process. In the build phase, C legitimately ob-
3: Initialise empty database XDB
tains search tokens for its own conjunctive queries and sends those Server + Colluding Client
to S for searching. S honestly executes the search routine but at 4: for = 1 to do
the same time records the xtag access from XSet (as a semi-honest Colluding Client
entity, it executes the search according to the protocol). Since C
$ ∗
5: Generate a random query ←− Δ ⊲ Combination of keywords
colludes with the S, C provides the server with the exact query ws
from Δ
it sent the search tokens for (without shufÒing). S associates the 6: Obtain search tokens tk for from G

recorded xtags with received query ws and stored locally for later
7: Send and tk (without shufÒing) to S

references. C can repeat this process multiple times to obtain mul-
Server
tiple (w,xtag) mappings, and S can grow the recorded information 8: Recover xtags using tk for w ∈ available from sent by

covering more ws.
C
Whilelaunching the attack on a benign client C , S compares
9: Set XDB[xtag ] = w ,∀w ∈ received from C
the xtags generated for the search tokens of C . If the xtags match,

Scaninferthecorresponding w from the recorded database with 10: AttackPhase
high probability. Observe that if colluding C and S can cover the Benign Client
11: Obtain search token for = w ∧ ... ∧ w from G
complete Δ, S would be able to recover all query keywords of C 1
12: Send to S
with complete certainty. We formalise this attack method below. Server
13: Computethextagsfrom
14: Look-up XDBusingthecomputedxtags:w = XDB[xtag ]
### 3.1 Formalising MC-ODXTAttackProcess
15: Repeat this for all xtags to recover W = {w ,...,w }
Wedenoteasemi-honestclient using C that colludes with a semi- 2
16: Return W
honest server S and a benign client using C. We assume that the
colluding client C shares the query keywords for which it received
100
the query tokens tk with S (without shufÒing) as well while execut- (%) 80 MC-ODXT
ing the Search routine as specified. Upon receiving the (w,tk), S 60
buildsalocaldatabaseXDBthatstoresrecordsoftheform (w,xtag). accuracy40
Weassumethat C makes queries during XDB building phase. We
Attack20
summarise the attack process (titled CrossAttack) formally in 0
Algorithm 1 below. 3 8 15 20 30 40 50
TheCrossAttackattackinAlgorithm1hastwophases-the Numberofqueries(×103)
build phase, where the colluding C engages with S to build the

XDB. In the attack phase, S obtains the xtags corresponding to Figure 1: Attack accuracy vs number of queries by the semibenign C ’s query, and looks-up XDB to recover the ws in. The
honestclient in the building phase. The number of queries
attack accuracy (probability of exact keyword recovery) improves bythebenignclientswas2000.
asmoreuniquewsfromΔarecoveredinthebuildphasetopopulate
XDB.Therefore, increasing the number of query iterations in the attack accuracy, defined as the ratio of the number of correct xbuildphaseleadstohighersuccessfulkeywordrecoveryasmorews term looked up to the total number of x-terms looked up, is plotted
are covered in XDB. The attack perfectly recovers all cross-terms in Figure 1 against the number of benign clients queries in the
with probability 1 for the ideal case when XDB contains all ws of Δ. building phase. The attack accuracy improves as the number of
### 3.2 ExperimentalEvaluation queries in the building phase increases, allowing the S to cover
more keywords in XDB. In this evaluation, the CrossAttack of
Weexecutedtheattack in Algorithm 1 on MC-ODXT to highlight Algorithm 1 successfully recovered more than 50% of the x-terms
the severity of the leakage discussed above. We used the Enron of benign clients’ queries.
email dataset for this experiment, and the platform details for this 3.3 ChallengesinDesigningMulti-clientSSE
experiment are available in Section 5. The experiment builds XDB
fromtherecordedxtagsandtheassociatedws.Subsequently,inthe Developing a multi-client SSE construction (MRSW or MRMW)
attack phase, the xtags corresponding to a benign client’s queries poses several challenges as a multi-client-specific workflow funare recorded and looked up in XDB for successful w recovery. The damentally differs from an SRSW construction. As illustrated by
Tokenised Multi-client Provisioning for Dynamic Searchable Encryption with Forward and Backward Privacy ASIACCS’24,July1–5,2024, Singapore, Singapore
the attack above, trivial extensions like MC-ODXT suffer from into Nomos. The core structure of the basic construction follows
multi-client specific attack(s), which needs to be suitably addressed fromODXTconstruction,andweencouragethereaderstorefer[30]
without compromising functionality or efÏciency. At a high level, for more details.
the following multi-client-specific privacy notions are necessary Clients.Weassumethereare clients{C ,...,C }whoareallowed
for a multi-client construction. 1
to obtain search tokens and search over the database. Each C can
Queryprivacy.Alegitimate client needs to share query information with the data owner, but the data owner must not be able to requestasearchtokenfollowingtheGenTokenroutineandengage
figure out which keywords are being queried. in the Search protocol with the server to retrieve query results.
Preventingtokenforgery.Anadversarialclient must not be able Gate-keeper. We denote the data owner using gate-keeper (deto modify or reuse received query tokens with previously obtained notedbyG)whocanupdateEDBandissuesearchtokenstoC(the
(or future) query tokens5. gate-keeper name signifies additional responsibility to generate
Token validation. The server should be able to validate that it search tokens for Cs). G holds the secret key (sk) to generate the
received a genuine query token from a client generated by the data search tokens and update the database. Since Nomos is an MRSW
ownerandnotbyathirdparty. construction, G is the only entity allowed to update EDB and is
Theaboveprivacyrequirements are provisioned in MC-ODXT considered a trusted party. Note that, although G is considered a
setting through a two-party oblivious computation-based mecha- trusted entity who can “see” the data, Nomos ensures query privacy
nism,morepreciselythroughOPRF.Inthatcase,Cdoesnothaveto of clients by not revealing query keywords to G.
share the actual with G. Instead, C shares hashed values mapped Trust in G We stress here that although G is a trusted entity, it
to group elements with G. However, in a dynamic construction does not learn the client’s search result, along with not knowing
following the ODXT structure, it needs to generate several bstags the query keywords. Thus, G is trusted for updates only. This trust
(corresponding to each update operation of the s-term) and addi- level in the MRSW setting is aptly applicable to real-life examples,
tional deblindings for these tokens, which requires modifications where G can be considered an administrative entity, such as the
of the approach of [23]. government or an employer, who can update the database and
Ourfinal construction Nomos adopts a similar approach to pro- enforce search policies on the clients accessing the data.
vision multi-client search, and an AE-based authentication method Server. The server (denoted by S) stores the encrypted database
is incorporated into the token generation process to validate query EDBcomprisedof TSetandXSetandperformsanupdateorsearch
tokens on the server side. However, the leakage from cross-terms as requested. S engages in the Update protocol with G to update
in the multi-client settings poses further challenges that need to be EDB. During a search, S interacts with C to receive the search
addressed without compromising efÏciency and security. tokensandperformsthedatabaselook-up.AttheendoftheSearch
Observe that the leakage mentioned in Section 3 appears due to protocol, it returns the retrieved encrypted ids to C matching the
a (w,id) pair validation requiring a valid physical location look-up actual query.
in the XSet storage, which is deterministic across multiple queries Weelucidate the MRSW setting here for better clarity and unfrom different clients. Therefore, S can record this information derstanding. Consider a genome analysis service provider offering
and exploit later as demonstrated in CrossAttack of Algorithm 1. a cloud-based gnome referencing service for clients who can query
To prevent this leakage, the XSet look-up access pattern needs overstandardgenomedataprovidedbytheanalysisservice.Followto be hidden from S. In our construction Nomos, we opt for a ing the current cloud-based service trend, assume that the genome
redundancy-based mechanism for XSet look-up that produces dif- analysis service has outsourced the infrastructure support to a
ferent access patterns for the same (w,id) pair. third-party cloud storage and computing resource provider, such
Note. We would like to mention that in this work, we specifically as Amazon AWS. In this example, the genome service provider
focus on cross-term-based leakage. Since the s-terms have a lower can be modelled as G, the cloud server acts as S, and the clients
frequency, the chance of s-terms colliding across queries from mul- requesting for look-up can be considered as Cs. Naturally, genome
tiple clients compared to x-terms is low. Thus, this type of leakage data is considered sensitive private information, which needs to be
is more severe for x-terms, and we prioritise mitigating x-term stored on S in encrypted form, and a C needs to query the data for
leakage in this development. We leave devising a similar strategy reference information. Such applications can be aptly handled by a
for s-terms as an important future work. scalable MRSW SSE scheme like Nomos.
## 4 NOMOS-DYNAMICMULTI-CLIENTSSE NomossettingassumesS asasemi-honestpartyandtreatseach
client as a semi-honest party individually (who can potentially col-
CONSTRUCTION lude with S while following the Nomos description as specified).
Westart by outlining the setting of our main construction with Gisatrusted entity that can update the encrypted database and
brief details of each entity and how each entity interacts with other generate search tokens for C’s queries (as G holds the secret keys).
entities. We discuss Nomos construction in two phases - the first Themulti-client provisioning in Nomos follows the approach [23]
phasedescribesthemulti-client provisioning, and the second phase andincorporates modifications for dynamic updates. Note that a
discusses the cross-term leakage mitigation technique incorporated de-centralised trust in G is ideal for the MRMW setting, where
multiple parties update the encrypted database. In contrast, the
5Note that, token forgery implies the presence of a malicious client; whereas the MRSWsettingallowsonlyonepartytoupdatethedatabase-typiattack in Algorithm 1 requires only a colluding semi-honest client. Nonetheless, our cally the data-owner. Thus, the MRSW setting allows provisioning
mainNomosconstructionconsiders token forgery prevention as a necessary feature
in the multi-client setting. multi-client search using basic OPRF primitive rather than relying
Algorithm2NomosSetup be recomputed from search tokens obtained via OPRF evaluations.
Input: Security parameters Note that, Algorithm 3 incorporates the RBF’s (discussed in Sec-
Output: sk, UpdateCnt, and EDB tion 4.2) redundant xtag generation process. The changes in Nomos
1: function Nomos.Setup algorithm(s) from MC-ODXT are highlighted in red.
Gate-keeper
∗
2: Sample a uniformly random ley from Z for OPRF 4.2 Mitigating Cross-Term Leakage

3: Sampletwosetsofuniformlyrandomkeys = {1,...,}
Recall from Section 3 that the cross-term leakage arises from reand = {1 , . . ., } from (Z∗ ) for OPRF
peated xtag accesses (translated to memory location accesses) by
4: Sample uniformly random key from {0,1} for PRF
S for the same (w,id) combinations from different queries (and
5: Sample uniformly random key from {0,1} for AE
updates). Intuitively, to mitigate this leakage, these memory ac-
6: Initialise UpdateCnt, TSet, XSet to empty maps cesses (to the same address for a particular (w,id) pair) need to
7: Gate-keeper keeps sk = ( , , , ); UpdateCnt is disclosed
be different for each access without affecting the look-up perforto clients when required, and is shared between gate-keeper
andtheserver mance severely. We adopt a simple yet effective way to achieve
8: Set EDB = (TSet,XSet) this through redundant location accesses, where multiple “copies”
9: Send EDBtoserver of the XSet bit value are stored at multiple addresses. A random
subset of these locations is looked up in each subsequent access for
Algorithm3NomosUpdate the same (w,id) pair.
1 1 RandomisingXSetaccess.WeoptforaBloomfilter(BF)(which
Input: = { ,..., }, = { ,..., }, accessed as [(w)]
physically stores XSet) based solution to achieve this redundant
and [(w)] for attribute (w) of w, ℓ is the number of hash
look-up. At a high level, a BF uses different hash functions to
functions for insertion into RBF, (w,id) pair to be updated, update generate distinct addresses for an element look-up. However,
operation op straightforwardly plugging in BF into MC-ODXT does not hide the
Output: Updated EDB repeated access pattern as addresses for a particular (w,id) pair
1: function Nomos.Update are still generated from the same xtag. We modify the BF structure
Gate-keeper slightly in the following way. Instead of using hash functions
2: Parse sk = ( , , ) and UpdateCnt

to generate the BF addresses for look-up, we use ℓ hash functions
3: Set ←(((w)) ,1)
to generate the BF addresses for an input element, where ℓ > .
4: If UpdateCnt[w] is NULL then set UpdateCnt[w] = 0
5: Set UpdateCnt[w] = UpdateCnt[w] +1 During a search, instead of using all ℓ hash functions to generate
[ (w)]
6: Set addr = ((w||UpdateCnt[w]||0)) the BF addresses, a subset of hash functions out of the ℓ are
[ (w)]
7: Set val = (id||op) ⊕ ((w||UpdateCnt[w]||1)) chosen randomly to generate the BF addresses. Observe that, with
8: Set = ( , id||op) · ( ( , w||UpdateCnt[w])−1)
this modification, S receives a different set of BF addresses for
[ (w)]· ( ,id||op)·
9: Set xtag = (w) , where ∈ [ℓ]
each repeated access of a particular (w,id) pair and hence can not
10: Send (addr,val,, {xtag } ) to server
Server ∈ [ℓ ] correlate amongpreviouslyaccessedentries.WecallthisBFvariant
11: Parse EDB = (TSet,XSet) Redundant Bloom Filter (RBF), and we present elaborate details
12: Set TSet[addr] = (val,) andanalysis of RBF in Appendix C.
13: Set XSet[xtag ] = 1, for ∈ [ℓ] Avoidingtworounds.NotethatincorporatingRBFasamodule
into Nomoswouldincuratwo-roundsolutionastheRBFaddresses
needtobegeneratedfromxtags.Thextagsmustnotberevealedto
onindependent system-oriented approaches like trusted execution S, and hence need to be generated on the C’s side. This is undesirenvironments or advanced primitives like MPC, as it handles up- able in a multi-client setting due to communication/computation
dates only from the data-owner, unlike the MRMW setting. This overhead and increased leakage from additional token exchanges.
modelisadoptedinexistingworkslikeOSPIR-OXT[23],whichwe WeavoidthisbyembeddingtheRBFaddressgenerationphaseinto
have followed here. the Update and GenToken algorithms in the following way.
[ (w)]· ( ,id||op)·
G(Update) : xtag = (w) , ∈ [ℓ]
### 4.1 SetupandUpdate
The Nomos Setup routine of Algorithm 2 is executed by G that G(GenToken) : bxtrap′ = bxtrap′ ∪ {(bxtrap′) }
initialises the system (including EDB on S). Subsequently, G and The revised final Update and GenToken algorithms are pre-
Scanjointlyexecute NomosUpdateofAlgorithm3repeatedlyon sented in Algorithm 3 and 4, respectively. The Search routine is
the data records from DB. modified to compute final addresses for RBF and is presented in
Update process. The Update algorithm is invoked by G with Algorithm 5 in Section 4.3.
(w,id) and op as input. S receives the encrypted values, along with Since Updateprotocolshouldbeexecutedinbatchesofmultiple
tags generated by G and updates the TSet and XSet. The Update deletions and additions involving several (w,id) pairs (a realistic
process of Algorithm 3 adopts the update routine of ODXT with assumption stated in Section 2), several XSet addresses are genermodifications to support multi-client search. The modifications ated for inserting multiple (w,id) pair records into RBF-based XSet.
include the way the TSet and XSet addresses (stags and xtags) are Thegenerated XSet addresses (for all (w,id) pairs) must be shufÒed
generated, such that in the Search routine, the same addresses can by G prior to sending to S in batches. This random shufÒing is
Tokenised Multi-client Provisioning for Dynamic Searchable Encryption with Forward and Backward Privacy ASIACCS’24,July1–5,2024, Singapore, Singapore
necessary to prevent S from associating any XSet access pattern Algorithm4NomosGenToken
to a probable keyword. In contrast, such shufÒing in MC-ODXT is Input: = {w ,· · · ,w } ( keywords in ), P is the set of allowed
ineffective against S associating a probable x-term to an observed 1
attribute sequences, ℓ and hashes are used for insertion and query
(or a set of observed) XSet address as only one single xtag match is in RBF, respectively
required for a particular (w,id) pair update and search. Output: strap, bstag , · · · ,bstag , , · · · , , bxtrap , · · · , bxtrap ,
1 1 1
env
4.3 TokenGenerationandSearch 1: function Nomos.GenToken
The multi-client search process starts with the token generation Client
process outlined in Algorithm 4 - a two-party protocol between a 2: Set = UpdateCnt[w1] ⊲ the update count of the least frequently
updated w
C and G. We briefly summarise the workflow of the GenToken $ ∗
3: Sample1, · · · , ←− Z
method of Algorithm 4 that generates the search tokens while
$ ∗
4: Sample , · · · , ←− Z
maintaining the query privacy of legitimate clients and preventing 1
token forgery by an adversarial client. 5: Set = ( (w )) , for = 1, · · · ,
6: Set = ((w ||||0)) , for = 1, · · · ,
1
Tokengenerationphase.TheNomosSearchalgorithmfollows 7: Set = ((w ||||1)) , for = 1, · · · ,
the ODXT [30] Search process, which generates two types of 1
8: Set av = ( (w ), · · · , (w )) = ( , . . ., )
1 1
search tokens – the stags and the xtraps. The stags are generated Gate-keeper
from the s-term (the least-frequently updated term or w1 in Al- 9: Abort if av ∉ P $
gorithm 4, without loss of generality), which are used to retrieve ∗
10: Sample 1, · · · , ←− Z

encrypted ids through TSet look-up. Whereas xtraps are generated $ ∗
11: Sample , · · · , ←− Z
from x-terms which are used to check the validity of a (w,id) pair 1
′
through XSet look-up. The GenToken routine in Nomos is respon- 12: Set strap = (1)
′ [1]·
sible for generating these tokens for multiple clients. Since the G 13: Set bstag = ( ) , for = 1, · · · ,
′ [1]
holds the keys ( , ) as a part of the secret key sk to generate 14: Set = ( ) , for = 1, · · · ,
′ [ ]·
the tokens, C needs to send the query to G to generate tokens 15: Set bxtrap = ( ) for = 2, · · · ,
$
without revealing the actual ws. We resort to an OPRF-based com- 16: Sample random indices for RBF ←− [ℓ], ∈ []
putation, allowing C to send query ws in blinded form. The major 17: for = 2 to do
′
difference fromOSPIR-OXT[23]isthatODXTgeneratesanstagfor 18: bxtrap = {}
′ ′ ′
each update count for the s-term, whereas OSPIR-OXT generates a 19: bxtrap = bxtrap ∪ {(bxtrap ) }, for ∈ {1, . . ., }
single stag (strap in GenToken). This is a direct consequence of 20: Set env = AE.Enc ( , · · · , , , · · · , )
1 1

the dynamic update capability of ODXT, and GenToken routine 21: Send(strap′, bstag′, · · · ,bstag′ , ′, · · · ,′ ,
′ 1′ 1
computes the blinded exponentiations for each stag. Similarly, C bxtrap , · · · , bxtrap , env) to client
Client2
also computes the blinded xtraps and the set of keyword attributes −1
av = { , . . . , } where = (w ) for ∈ [], which are sent to G. 22: Set strap = (strap′)1
1 −1
Blinded tokens and query validation. Upon receiving the search to- 23: Set bstag = (bstag′ ) , for = 1, · · · ,
−1
kens, G first verifies whether av is a valid set of attributes which 24: Set = (′ ) , for = 1, · · · ,
C is allowed to query by checking av ∈ P. If not valid, G aborts
25: for = 2 to do
the process. Otherwise, G computes its own part of the OPRF 26: Initialise bxtrap = {}
computation (party B’s computation in OPRF as discussed in Sec- 27: for = 1 to do −1
tion 2) by processing bstrap, bstag and bxtrap. The blinded strap 28: bxtrap = bxtrap ∪ {(bxtrap′[][]) }
(bstrap′) computation is done through OPRF evaluation using ,
29: Output (strap, bstag , · · · ,bstag , , · · · , ,
1 1
andblinded stag (bstag′) and xtrap (bxtrap′) generation are done bxtrap , · · · , bxtrap , env) as search token
throughOPRFevaluationusing and combinedwithGsown 2

blinding factors { , . . ., } and { , . . . , }. G’s blinding factors
1 1
s and s are necessary to prevent a potentially malicious client anddeblinding during Search execution. However, S itself is not
from modifying the search tokens by replacing the search tokens. involved in the GenToken protocol. The AE decryption key is
Since the blinding factors are randomly generated for each request, generated by G at Setup and shared with S.
apolynomiallyboundmaliciouspartycannotreplicatetheblinding
factors. S can verify the tokens as G encrypts { ,..., } and Search phase. The Nomos Search of Algorithm 5 is jointly ex-
1
{ , . . . , } using AE that S can authenticate prior to search (in ecuted by a C and S without any involvement of G. However, C
1
the Search routine). musthaveobtainedthesearchtokensfrom G priortoinvokingthe
In the final phase of GenToken routine, C deblinds the doubly- Searchroutine. In this phase, the client sends the blinded search

blinded bstag′s, s and bxtrap′s using its own blinding factors tokens and encrypted blinding factors to S that it received from
( , . . . , ) and ( , . . . , ) to obtain the G-blinded tokens (strap, Gattheendof GenToken(blindedwith G’sblinding factors). At
1 1
bstag and bxtrap), which C subsequently uses as the search token. a high level, the Search protocol proceeds in two stages - first, C
Note that S receives the AE-encrypted blinding factors from G computes the final xtraps from the received bxtraps. Note that the
as a part of the search token, which are used for token validation resulting xtokens are still blinded as C does not have G’s blinding
Algorithm5NomosSearch S-term information to clients. In this multi-client setting we
assumethat C ’s obtain the s-term frequency information from G
Input: ,strap, bstag , · · · ,bstag , , · · · , , bxtrap , · · · , bxtrap ,
1 1 1 via a suitable privacy-preserving mechanism without revealing the
1, . . . , , env, UpdateCnt keyword to G. This a reasonable assumption following from the
Output: IdList prior works including OXT [9], OSPIR-OXT [23], HXT [27], and
1: function Nomos.Search ODXT[30](asthestatic constructions do not have update capabil-
Client ity, they use keyword frequency instead of the update frequency).
2: Set ←(strap,1)

3: = UpdateCnt[w ] Weelaborate more on possible privacy-preserving mechanisms for
1
4: Initialise stokenList to an empty list frequency information retrieval (such as based on private informa-
5: Initialise xtokenList , · · · , xtokenList to empty lists
1 tion retrieval [2, 13, 29]) in Appendix B.1.
6: for = 1 to do
7: stokenList = stokenList ∪ {bstag } 4.4 ComputationandStorageOverhead
8: for = 2 to do The following overhead analysis assumes that a single record in
9: xtokenSet ←{}
, TSet or XSet requires constant storage, and the group operations
10: for = 1 to do
( , ||)
1 andstorage look-ups are the costliest operations in practice.
11: Set xtoken =bxtrap []
,

12: Set xtokenSet =xtokenSet ∪xtoken
, , , Computationoverhead.TheUpdateroutineexecutesfora(w,id)
13: Randomlypermutethetuple-entries of xtokenSet
14: Set xtokenList = xtokenList ∪xtokenSet , pair in each invocation. The Update routine computes the TSet
, addresses along with w-bound deblinding factor, which requires a
15: Send (stokenList,xtokenList , · · · ,xtokenList )
1 total of three hash computations, two group operations and field
Server inversion. However,asweuseRBF-basedXSet,ℓ xtagcomputations
16: Uponreceivingenvfromclient,verifyenv;ifverificationfails,return require ℓ group operations that dominates the Update routine with
⊥; otherwise decrypt env (ℓ) computation overhead. Since ℓ is a constant (which is signif-
17: Parse EDB = (TSet,XSet) icantly small compared to the number of updates) for a specific
18: Initialise sEOpList to an empty list
19: for = 1 to stokenList. do setting, this (ℓ) can be asymptotically approximated to (1) per
20: Set cnt = 1 Updateinvocation for a series of updates.
21: Set stag ← (stokenList[])1/ TheGenTokenprotocolrequires || +2|UpdateCnt[w ]| hash
22: Set (sval , ) = TSet[stag ] 1
computations and group operations to generate the client-side
23: Initialise = 1 values with blinding. The gate-keeper-side processing involves
24: for = 2 to do ||+2|UpdateCnt[w ]|groupoperationsand||+|UpdateCnt[w ]|
25: Set xtokenSet =xtokenList [] 1 1
, field multiplications. The client-side deblinding phase computes
26: for = 1 to do || + 2|UpdateCnt[w ]| group operations. As a result, GenToken
27: Computextag = (xtokenSet [ ]) / 1
, , incurs(|| + 2|UpdateCnt[w ]|) computation overhead asymp-
28: If XSet[xtag ] = 0, then set = 0 ⊲XSetisimple- 1
, totically that is sublinear in the total database size |DB|. The commented using RBF munication overhead is also(|| + 2|UpdateCnt[w ]|) as C and
29: If = 1, then set cnt = cnt + 1 1
30: Set sEOpList = sEOpList ∪ {(,sval,cnt)} Gexchange || + 2|UpdateCnt[w ]| tokens in this process.
31: Sent sEOpList to client 1
Client TheSearchprotocolcomputes·||·|UpdateCnt[w1]|groupop-
32: Initialise IdList to an empty list erationstocomputetheblindedxtokens.Sperforms|UpdateCnt[w1]|
33: for ℓ = 1 to sEOpList. do TSet look-ups that require |UpdateCnt[w1]| group operations for
deblinding.Additionally,S computesatotal·||·|UpdateCnt[w ]|
34: Let (, sval , cnt ) = sEOpList[ℓ] 1
XSet addresses for look-up. Therefore, Nomos Search incurs( ·
35: Recover (id ||op ) = sval ⊕ ℓ || · |UpdateCnt[w ]|) asymptotic computation overhead with all
36: If op is DEL and cnt = then set IdList = IdList \ {id } 1
37: Output IdList combined. Since is a small constant, the Search overhead is
sublinear in the total database size |DB|. Furthermore, C needs
to send ( · || · |UpdateCnt[w ]|) tokens to S, and it receives
1
factors. S receives the bstags and computed xtokens along with G’s (|UpdateCnt[w1]|) encrypted values back as the result. Hence,
AE-encrypted blinding factors. S validates the AE ciphertext using theasymptoticcommunicationoverheadof NomosSearchroutine
key and proceeds for decryption if the validation is successful. is ( · || · |UpdateCnt[w1]|).
Storage overhead. We analyse the Nomos EDB storage overhead
S deblinds the received bstags to recover the actual stags, and with respect to the plain database DB. The storage overhead for
after that, it follows the usual ODXT search routine to retrieve the
matching ids. During xtag computation, S deblinds xtokens using EDBinNomosisessentiallythecombinedTSetandXSetoverhead.
the decrypted G’s blinding factors, and follows the usual ODXT The TSet overhead of Nomos is practically the same as of single
search process6. client dynamic construction ODXT, which is (|DB|) (linear in
termsofthenumberofrecordsintheplaindatabaseDB)astheTSet
6Weemphasise that Nomos follows the vast majority of the SSE literature (in- stores one encrypted value for each entry in DB. The RBF-backed
cluding ODXT itself) in its index-only focus and does not incorporate a dedicated XSetrequiresℓ ·(|DB|) storage. However, compared to TSet, XSet
mechanismtohandleactual document retrieval. We leave extending Nomos to full
SSEschemewithfinalencrypted document retrieval as an interesting future work. stores only 1/0 for each index and requires lesser storage than TSet
Tokenised Multi-client Provisioning for Dynamic Searchable Encryption with Forward and Backward Privacy ASIACCS’24,July1–5,2024, Singapore, Singapore
(%)100 MC-ODXT Nomos Nomos
80 Nomos( = 8,ℓ = 12) time ODXT time 104 ODXT
60 Nomos( = 8,ℓ = 24) 3s) 4 MC-ODXT 3s) MC-ODXT
accuracy40 −1010 −10
× ×
( ( 2
## 20 End-to-end End-to-end10
Attack0 102
3 8 15 20 30 40 50 46 60 100 200 500 1000 160025003906 4 8 16 32 64 110 170
Numberofqueries(×103) s-term update frequency s-term update frequency
Figure 2: Attack accuracy vs number of Figure 3: End-to-end query latency for Figure 4: End-to-end query latency for
queries by the colluding client in the two-keyword queries of the form = two keyword queries of the form =
build phase. The number of queries by w ∧w (s-termw updatefrequencyis w ∧w (s-termw updatefrequencyis

the benign clients was set to 2000. fixed at 70). varied).
## 105 Nomos Nomos Nomos
ODXT 5 ODXT 5 ODXT
times)10 times)10
(KB)103 MC-ODXT 3 4 MC-ODXT 3 4 MC-ODXT
−1010 −1010
erhead × 3 × 3
v ( 10 ( 10
Communicationo1 End-to-end End-to-end
10 2 2
26 50 100 200 500 1000 1650 2761 10 64 100 200 500 1000 2000 3450 10 11 20 50 70 100 120 144
s-term update frequency Keywordupdatefrequency s-term update frequency
Figure 5: End-to-end communication Figure 6: End-to-end query time for Figure 7: End-to-end query time for
overheadfortwo-keywordqueriesofthe multi-keyword queries of the form = multi-keyword queries of the form =
form = w ∧w (s-termw updatefre- w ∧...∧w (s-termw updatefrequency w ∧...∧w (s-termw updatefrequency
1 1 1 1
quencyisvaried). is fixed at 60). is varied).
5 5
## 10 Nomos Nomos (MB)3 Nomos
ODXT 105 ODXT 2 ODXT
(KB) 3 MC-ODXT (MB)4 MC-ODXT 1 MC-ODXT
10 storage|10 storage
er 0.5
v
erhead EDB 3
v | 10
o 1 Ser 0.2
Communication10
102 Client-side0.1
26 50 100 200 500 1000 1700 2944 0.8 2 5 10 15 18 13 20 40 80 160 280
s-term update frequency Numberofuniquew-idpairsinDB(×106) NumberwsinDB |Δ| (×103)
Figure 8: End-to-end communication Figure 9: Server-side storage overhead Figure 10: Client-side storage overhead
overheadformulti-keywordqueriesof (EDB size) for Nomos, MC-ODXT and for Nomos, ODXT and MC-ODXT for
theform = w ∧...∧w (s-termw up- ODXTforsameplaininputdatabasesize. sameplaininputdatabasesize.
1 1
date frequency is varied).
that stores encryptions of (|DB|) items. As a result, Nomos has TSet and XSet. We ran the experiments on dual 24-core Intel Xeon
linear (|DB|) asymptotic storage overhead in practice. E5-2690 2.6GHz CPU with 128GB RAM and 512GB SSD running
Security analysis. We divert the elaborate security analysis of Ubuntu20.04 64bit operating system with gigabit network link.
Nomostothefullversion of the paper1 due to lack of space. Queryprocessing.WeevaluatedNomos’sperformancefortwo
5 IMPLEMENTATIONDETAILSANDRESULTS differenttypesofqueries-two-keywordandmulti-keywordqueries.
Thetwo-keywordqueriesareoftheform = w ∧w ,whichwe
1 2
In this section, we describe a prototype implementation of Nomos represent as = w ∧ w or = w ∧ w . Here w is called

andevaluateitsoverheadandperformanceoverreal-worlddatabases. the constant term whose frequency is kept fixed, and w is the
Datasetandplatform.WeusedtheEnronemaildataset7 forour variable term whose frequency is varied during experimentation.
For the multi-keyword queries of the form = w ∧ ... ∧ w , ∈
experiments.Thedatabasecontains517,401documents(emails)and 1
[3, 6], the first keyword w is varied and maximum frequency of
20 million keyword-document pairs, with a total size 1.9 GB. The 1
{w ,...,w } is fixed in one set of experiments. In another set, the
final Nomos algorithm was implemented using C++11 with native 2
frequency of w is kept fixed and max frequency of {w ,...,w }
multithreading support and was compiled using GCC9. We used 1 2
Redis as the database backend system to store EDB comprising is varied. These experiments examine the sublinear search and
communication overhead of Nomos for two and multi-keyword
7https://www.cs.cmu.edu/~enron queries. The query keywords are sampled randomly from Δ.
### 5.1 ExperimentsonLeakage storage overhead with ODXT to illustrate the storage overhead as
Weexecuted the CrossAttack method of Algorithm 1 on Nomos a trade-off with lesser leakage. The EDB overhead for both Nomos
to compare the leakage with MC-ODXT. The attack accuracy is and ODXTareplotted in Figure 9, and the client-side storage overplotted in Figure 2 against the number of queries issued by the head is plotted in Figure 10. Observe that the storage overhead
colluding client in the build phase of the attack. Clearly, Nomos profile for both Nomos and ODXTremainslinearwithDBsize,and
has a significantly lower attack accuracy compared to MC-ODXT. NomosEDBoverheadisapproximately2.5timesof ODXTwhichis
This low attack accuracy is a direct consequence of the redundancy manageableonthecloudinpractice.Allthreeconstructionsrequire
of RBF during XSet accesses. The value of the RBF parameter ℓ was (|Δ|) client-side storage as illustrated in Figure 10.
set to 12, while the parameter was set to 8. Thus, Nomos achieves Theperformanceoverheadof Nomosisslightlyhighercompared
morethan50%reductioninattackaccuracywithfouradditional to MC-ODXTasNomosgeneratesmoretokensduetoRBF-based
indices for XSet insertion. The parameter needs to be kept at a XSet look-up. The increased performance and storage overhead of
fixed value to maintain a desired false positive rate for the same Nomosisanecessaryleakage-versus-overhead trade-off to allow
database parameters and experiment setting as of the non-RBF secure searches in the multi-client setting of Nomos. The storage
version. In contrast, ℓ is responsible for the redundancy in RBF overhead of Nomos is less than 2×-2.5× of ODXT (and MC-ODXT)
leading to a lower attack accuracy due to the increased redundant for storage that is practically manageable in a cloud infrastructure.
accesses per (w,id) pair. However, a high value of ℓ would incur Comparedwiththeplainversionofsearch,encryptedsearchincurs
larger storage to accommodate additional XSet entries, and thus higheroverheadwhichvariesdependinguponthecryptographicpaimplies a trade-off. We view this as a leakage-versus-storage trade- rameters/algorithms used, data structure, and the database system
off in the multi-client setting that is unavoidable in practice. We used. However, it provides strong confidentiality against unauthopresent comprehensive discussion on the choice of parameters and rised access compared to the typical unencrypted search process
analysis of RBF in Appendix C. andincurslessleakageandcommunicationoverheadthanthenaïve
symmetrically encrypted database with trivial decryption.
### 5.2 ExperimentsontheSearchLatency In summary, Nomos provides secure multi-client search with
Weconsideredtwotypesofqueriestoevaluate the search perfor- dynamicupdatesattheexpenseofminimaladditionalstorageovermanceof Nomosasstatedearlier in this section. For two-keyword head. Modern cloud services can easily manage this additional
queries, we fix the frequency of the constant term w and vary the storage to provide a secure environment to process encrypted data
which multiple users can access. Naturally, depending upon the
frequency of the variable term w from 10 to 5000. The end-to-end requirement, a service provider needs to make necessary modificasearch latency for the queries of the form = w ∧ w in Figure 3
tions to the core algorithms. These modifications mainly include
andqueries of the form = w ∧w in Figure 4. Observe that, in
parsing the data into a suitable format to store and process as a
Figure 3, the end-to-end search latency remains almost constant. multi-map. The data owner is responsible for this pre-processing
Whereas in Figure 4, the search latency varies linearly with the of unstructured data to be updated into the encrypted database on
frequency of the variable term. This behaviour validates the sub- the remote server. Thus, in general, Nomos can be adopted in a
linearity of the Nomos search algorithm where the search latency broad set of practical applications with minimal modification, such
linearly dependsonthefrequencyofthes-termof |DB(w1)|,which as healthcare, government records, and banks, to name a few.
is sublinear in terms of total number of records in the database.
Thecommunicationoverheadsof NomosGenTokenandSearch 6 CONCLUSIONANDFUTUREDIRECTIONS
are plotted in Figure 5 for two-keyword queries. Nomos incurs sublinear communication overhead (linear in terms of s-term update We introduced the first forward and backward secure dynamic
frequency) for GenToken and Search as shown in the plot. How- multi-client SSE scheme Nomos supporting conjunctive Boolean
ever,incomparisonwithODXT,Nomoshastheadditionalnecessary queries. NomosisanMRSWconstructionthatbuildsuponthestateoverheadofsearchtokensgeneratedbyGenToken,andtheSearch of-the-art SRSWdynamicconstructionODXT[30].Weshowedthat
communication overhead increases due to RBF-based XSet. the straight-forward extension of ODXT to the multi-client setting
Wealsoreportexperimentalresultsformulti-keywordqueriesof is completely insecure against collusion between a semi-honest
the form = w ∧...w ,where ∈ [3,6],andwedenotew asthe client and a semi-honest server due to a cross-term–based leak-
1 1 age. Our Nomos construction mitigates this leakage by adopting a
s-terminthemulti-keywordqueries.Theend-to-endsearchlatency
for two sets of experiments is plotted for fixed and variable s-term customised Bloom filter called redundant Bloom filter while supupdate frequencies in Figure 6 and Figure 7, respectively. Observe portingefÏcientsingle-roundmulti-clientqueries.Wepresentedex-
that the search overhead remains sublinear (proportional to the tensive experimentation to demonstrate the practical performance
frequency of the s-term) in terms of the number of total records of Nomosoverreal-worlddatabases. We leave extending Nomos to
in EDB. Similarly, the communication overhead remains sublinear the MRMWsettingasaninteresting direction of future research.
in the total database size scaled by the number of cross-terms, as
illustrated in Figure 8. ACKNOWLEDGMENTS
5.3 Evaluation of the Storage Overhead Theauthors would like to thank the grant “Design and Implementation of EfÏcient and Secure Searchable Encryption” sponsored
Wevariedthenumberof wsinDBandgeneratedthecorrespond- by MHRD-STARS (Scheme for Transformational and Advanced
ing EDB by executing Nomos Update. We compare the Nomos Research in Sciences), India for partially supporting the work.
Tokenised Multi-client Provisioning for Dynamic Searchable Encryption with Forward and Backward Privacy ASIACCS’24,July1–5,2024, Singapore, Singapore
REFERENCES [34] Yupeng Zhang, Jonathan Katz, and Charalampos Papamanthou. 2016. All Your
[1] MegumiAndoandMarilynGeorge.2022. OntheCostofSuppressingVolumefor Queries Are Belong to Us: The Power of File-Injection Attacks on Searchable
Encrypted Multi-maps. Proceedings on Privacy Enhancing Technologies 4 (2022), Encryption. In USENIX Security Symposium.
44–65.
[2] AmosBeimelandYuvalIshai.2001. Information-theoretic private information A SECURITYGAMESFORDYNAMIC
retrieval: A unified construction. In ICALP.
[3] Mihir Bellare and Chanathip Namprempre. 2000. Authenticated encryption: MULTI-CLIENTSSE
Relations among notions and analysis of the generic composition paradigm. In
ASIACRYPT. WepresenttheRealandIdealsecuritygamesfordynamicmulti-
[4] Dan Boneh, Xavier Boyen, and Eu-Jin Goh. 2005. Hierarchical Identity Based client SSE as stated in Section 2.3 of the main manuscript.
Encryption with Constant Size Ciphertext. In EUROCRYPT. Games for adversarial client The Real and Ideal games for the
[5] Christoph Bösch, Pieter H. Hartel, Willem Jonker, and Andreas Peter. 2014. A
SurveyofProvablySecureSearchableEncryption. ACMComput.Surv.47(2014). security of a dynamic MRSW SSE scheme Π from an adversarial
[6] Raphael Bost. 2016. Σoo: Forward secure searchable encryption. In CCS. client are presented in Algorithms 6 and 7.
[7] Raphaël Bost, Brice Minaud, and Olga Ohrimenko. 2017. Forward and backward
private searchable encryption from constrained cryptographic primitives. In
CCS. Π
[8] David Cash, Joseph Jaeger, Stanislaw Jarecki, Charanjit S. Jutla, Hugo Krawczyk, Algorithm6ExperimentRealA() adversarial client
Marcel-Catalin Rosu, and Michael Steiner. 2014. Dynamic Searchable Encryption
in Very-Large Databases: Data Structures and Implementation. In NDSS. 1: function RealΠ ()
[9] DavidCash,StanislawJarecki,CharanjitS.Jutla,HugoKrawczyk,Marcel-Catalin A
Rosu, and Michael Steiner. 2013. Highly-Scalable Searchable Symmetric Encryp- 2: ← A()
3: (sk,st ,EDB ) ← Π.Setup(,)
0 0
tion with Support for Boolean Queries. In CRYPTO. 4: for ← 1 to do
[10] Javad Ghareh Chamani, Dimitrios Papadopoulos, Charalampos Papamanthou, 5: if query-type == gentoken then
6: ←A(,EDB , 1, . . . , )
andRasoolJalili. 2018. New Constructions for Forward and Backward Private −1 −1
7: (st ,t ) ← GenToken(sk,st , )
Symmetric Searchable Encryption. In CCS. −1
[11] Yan-ChengChangandMichaelMitzenmacher.2005. Privacypreservingkeyword 8: else if query-type == search then
9: ←A(,EDB , 1, . . . , )
searches on remote encrypted data. In ACNS. −1 −1
10: (st ,EDB ,DB( )) ← Search(sk,st , t ; EDB )
[12] Melissa Chase and Seny Kamara. 2010. Structured Encryption and Controlled −1 −1
11: denotes the view of the adversary after the th query
Disclosure. In ASIACRYPT.
12: ← A(,EDB ,1,..., )
[13] Benny Chor, Oded Goldreich, Eyal Kushilevitz, and Madhu Sudan. 1995. Private 13: return
information retrieval. In FOCS.
[14] Reza Curtmola, Juan A. Garay, Seny Kamara, and Rafail Ostrovsky. 2006. Searchable symmetric encryption: improved definitions and efÏcient constructions. In
ACMCCS.
[15] MohammadEtemad,AlptekinKüpçü,CharalamposPapamanthou,andDavid Algorithm7ExperimentIdealΠ () for adversarial client
Evans. 2018. EfÏcient Dynamic Searchable Encryption with Forward Privacy. A,SIM
PoPETS (2018).
[16] Sky Faber, Stanislaw Jarecki, Hugo Krawczyk, Quan Nguyen, Marcel-Catalin 1: function IdealΠ ()
Rosu, and Michael Steiner. 2015. Rich Queries on Encrypted Data: Beyond Exact A,SIM Setup Update GenToken Search
Matches. In ESORICS. 2: Parse the L as: {L , L , L , L }.
[17] Craig Gentry. 2009. Fully homomorphic encryption using ideal lattices. In ACM 3: ← A() Setup
4: (st , EDB ) ← SIM (L (, ))
SIM 0 0
STOC. 5: for ← 1 to do
[18] Craig Gentry, Amit Sahai, and Brent Waters. 2013. Homomorphic Encryp- 6: if query-type == gentoken then
7: ←A(,EDB , 1, . . . , )
tion from Learning with Errors: Conceptually-Simpler, Asymptotically-Faster, −1 −1
8: (st , t ) ←SIM (st , LGenToken( ))
Attribute-Based. In CRYPTO. SIM 1 SIM
[19] Eu-Jin Goh. 2003. Secure Indexes. IACR Cryptology ePrint Archive (2003). 9: else if query-type == search then
10: t ←A(,EDB , 1, . . . , )
[20] Oded Goldreich. 1987. Towards a theory of software protection and simulation −1 −1 Search
11: (st , EDB ,DB( )) ← SIM (st , L (t );EDB )
byoblivious RAMs. In STOC. SIM Search SIM −1
12: denote the view of the adversary after the th query
[21] Oded Goldreich and Rafail Ostrovsky. 1996. Software Protection and Simulation
13: ← A(,EDB ,1,..., )
onOblivious RAMs. J. ACM 43 (1996). 14: return
[22] Ariel Hamlin, Abhi Shelat, Mor Weiss, and Daniel Wichs. 2018. Multi-Key
Searchable Encryption, Revisited. In Public-Key Cryptography - PKC 2018 (Lecture
Notes in Computer Science). Springer. Games for adversarial server The Real and Ideal games for the
[23] Stanislaw Jarecki, Charanjit S. Jutla, Hugo Krawczyk, Marcel-Catalin Rosu, and
Michael Steiner. 2013. Outsourced symmetric private information retrieval. In security of a dynamic MRSW SSE scheme Π from an adversarial
CCS. server are presented in Algorithms 8 and 9.
[24] SenyKamaraandTarikMoataz.2017. BooleanSearchableSymmetricEncryption
with Worst-Case Sub-linear Complexity. In EUROCRYPT.
[25] SenyKamaraandCharalamposPapamanthou.2013. Parallelanddynamicsearchable symmetric encryption. In FC. Algorithm8ExperimentRealΠ () adversarial server
[26] Seny Kamara, Charalampos Papamanthou, and Tom Roeder. 2012. Dynamic A
searchable symmetric encryption. In ACM CCS. 1: function RealΠ ()
[27] Shangqi Lai, Sikhar Patranabis, Amin Sakzad, Joseph K. Liu, Debdeep Mukhopad- A
hyay,RonSteinfeld,ShifengSun,DongxiLiu,andCongZuo.2018. ResultPattern 2: ← A()
3: (sk,st ,EDB ) ← Π.Setup(,)
Hiding Searchable Encryption for Conjunctive Queries. In CCS. 0 0
[28] MoniNaorandOmerReingold.2004. Number-theoreticconstructionsofefÏcient 4: for ← 1 to do
5: if query-type == search then
pseudo-random functions. JACM 51 (2004). 6: ←A(,EDB , 1, . . . , )
−1 −1
7: (st ,EDB ,DB( )) ← Π.Search(sk,st , ; EDB )
[29] Rafail Ostrovsky and William E Skeith III. 2007. A survey of single-database −1 −1
private information retrieval: Techniques and applications. In PKC. 8: else if query-type == update then
9: (op , {w ,id }) ← A(,EDB , 1, . . . , )
[30] Sikhar Patranabis and Debdeep Mukhopadhyay. 2021. Forward and Backward −1 −1
10: (st ,EDB ) ←
Private Conjunctive Searchable Symmetric Encryption. In NDSS.
Π.Update(sk,st , (op , {w ,id });EDB )
[31] Phillip Rogaway. 2002. Authenticated-encryption with associated-data. In CCS. −1 −1
11: denotes the view of the adversary after the th query
[32] Dawn Xiaodong Song, David A. Wagner, and Adrian Perrig. 2000. Practical
12: ← A(,EDB ,1,..., )
Techniques for Searches on Encrypted Data. In IEEE S&P. 13: return
[33] Wolfgang Stadje. 1990. The collector’s problem with group drawings. Advances
in Applied Probability 22, 4 (1990), 866–882.
Algorithm9ExperimentIdealΠ () for adversarial server Algorithm11MC-ODXTUpdate
A,SIM Input: , = {1,...,}, = {1 ,..., }, accessed as [ (w)] and
1: function IdealΠ ()
A,SIM [ (w)] for attribute (w) of w, , (w,id) pair to be updates, update operation op
Setup Update GenToken Search
2: Parse LS as: { (L , L , L , L }. Output: Updated EDB
3: ← A() 1: function MC-ODXT.Update
4: (st , EDB ) ← SIM (LSetup(,)) Gate-keeper
SIM 0 0
5: for ← 1 to do 2: Parse ( , , ) and UpdateCnt

6: if query-type == search then
3: Set ←(((w)) ,1)
7: ←A(,EDB , 1, . . . , )
−1 −1 Search 4: If UpdateCnt[w] is NULL then set UpdateCnt[w] = 0
8: (st , EDB ,DB( )) ← SIM2(st , L ( ); EDB ) 5: Set UpdateCnt[w] = UpdateCnt[w] +1
SIM SIM −1
9: else if query-type == update then [ (w)]
10: (op , {w ,id }) ← A(,EDB , , . . . , ) 6: Set addr = ( (w||UpdateCnt[w]||0))
−1 1 −1 [ (w)]
11: (st ,EDB ) ← 7: Set val = (id||op) ⊕ ( (w||UpdateCnt[w]||1))
8: Set = ( , id||op) · ( ( , w||UpdateCnt[w])−1)
SIM1(st , LUpdate((op , {w ,id }));EDB )
SIM −1 [ (w)]· ( ,id||op)
12: denote the view of the adversary after the th query 9: Set xtag = (w)
10: Send (addr,val,,xtag to server
13: ← A(,EDB ,1,..., )
14: return Server
11: Parse EDB = (TSet,XSet)
12: Set TSet[addr] = (val,)
B MC-ODXTCONSTRUCTIONDETAILS 13: Set XSet[xtag] = 1
Wepresent MC-ODXT construction algorithm in this Appendix. Algorithm12MC-ODXTGenToken
MC-ODXTisanextension of ODXT [30] to multi-client MRSW
Input: = w ∧ ... ∧ w . P is the set of allowable attribute sequences, , , ,
setting following the OPRF-based approach of OSPIR-OXT [23]. 1
Output: strap, bstag , · · · ,bstag , , · · · , , bxtrap , · · · , bxtrap , env
The MC-ODXT Setup algorithm (Algorithm 10) executed by G 1 1 2
1: function MC-ODXT.GenToken
samples OPRF, PRF and AE keys. A client C engages with G in the Client
$ ∗
GenToken protocol (Algorithm 12) to obtain the blinded search 2: Pick1, · · · , ←− Z

tokens for a conjunctive query to search over the EDB. After ob- 3: Set = UpdateCnt[w1]
$ ∗
4: Pick , · · · , ←− Z
taining the search tokens, C engages with S in the Search protocol 1
5: Set ←((w )) , for = 1, · · · ,
(Algorithm 13) to retrieve the set of ids matching the conjunctive
6: Set ←((w ||||0)) , for = 1, · · · ,
1
query. G jointly executes the Update protocol (Algorithm 11) with 7: Set ←((w ||||1)) , for = 1, · · · ,
1
8: Set av = ( (w ), · · · , (w )) = ( , . . . , )
Stoinsert contents into or delete contents from EDB. Gate-keeper 1 1
Algorithm10MC-ODXTSetup 9: Abort if av ∉ P $ ⊲ Abort if attributes do not match
10: Pick 1, · · · , ←− Z∗

Input: $ ∗
11: Pick , · · · , ←− Z
Output: sk,UpdateCnt,EDB 1
′
1: function MC-ODXT.Setup 12: Set strap ← (1)
′ [1 ]·
Gate-keeper 13: Set bstag ← ( ) , for = 1, · · · ,
2: Sample a uniformly random key from Z∗ for OPRF ′ [ ]
14: Set ← ( ) 1 , for = 1, · · · ,
3: Sampletwosetsofuniformlyrandomkeys = {1,..., } and = [ ]·
15: Set bxtrap′ ← ( ) for = 2, · · · ,
{1 , . . . , } from (Z∗ ) for OPRF
16: Set env = AE.Enc ( , · · · , , , · · · , )
1 1
4: Sample uniformly random key from {0,1} for PRF ′ ′ ′ ′ ′ ′ ′
17: Send strap , bstag , · · · , bstag , , · · · , , bxtrap , · · · , bxtrap , env to Client
5: Sample shared uniformly random key from {0,1} for AE Client 1 1 2
−1
6: Initialise UpdateCnt, TSet, XSet to empty maps 18: Set strap ← (strap′)1
7: Gate-keeper keeps sk = ( , , , ); UpdateCnt is disclosed to clients when re-
−1
quired, and is shared between gate-keeper and the server ′
19: Set bstag ← (bstag ) , for = 1, · · · ,
8: Set EDB = (TSet,XSet) −1
9: Send EDBtoserver 20: Set ←(′) , for = 1, · · · ,

′ −1
21: Set bxtrap ← (bxtrap ) , for = 2, · · · ,

22: Output (strap, bstag , · · · , bstag , , · · · , , bxtrap , · · · , bxtrap , env as search
B.1 Private retrieval of s-term information token 1 1 2
As stated in Section 4.3 of the main body, the s-term update frequency requires a commonly accessible record in this setting. This
necessitates a secure mechanism to disclose the keyword frequen- frequency values, indexed by keywords, and the C wants to look
cies to prevent G from knowing C’s query keywords. Naïvely, this up the frequency of a particular keyword without revealing to
can be achieved via a publicly hosted website or storage with G the G what is the keyword being looked up. This lends itself to
havingthewritepermission(implicitlyadoptedbyOXT[9],OSPIR- a classic single-server PIR-based solution. In fact, one could also
OXT[23], HXT [27], and ODXT [30]). In this work we assumed use a multi-server PIR solution [2] where the G simply distributes
that C’s have some suitable mechanism to retrieve the frequency the frequency information across multiple (mutually distrusting)
information from G, and focused on the core construction to allow servers, thus decentralising the trust assumptions involved.
multi-client search capability. We note, however, that using a (multi-server) PIR-based fre-
Aplausible way to allow such frequency information retrieval quency information retrieval in the search token generation phase
in a privacy-preserving manner is to employ a private information brings in additional computation overhead, and possibly, additional
retrieval (PIR) [2, 13, 29] based mechanism involving a C and the G. rounds.Weleaveincorporatingadedicateds-termupdatefrequency
Theideais (at a high level) that the G holds an array of keyword retrieval mechanism as a part of the MRMW extension of Nomos.
Tokenised Multi-client Provisioning for Dynamic Searchable Encryption with Forward and Backward Privacy ASIACCS’24,July1–5,2024, Singapore, Singapore
Algorithm13MC-ODXTSearch Algorithm15BloomFilterQuery
Input: strap, bstag , · · · , bstag , , · · · , , bxtrap , · · · , bxtrap , env, UpdateCnt Input: Input parameters: x - element to be queried in BF
1 1 2 Output: Output parameters: True/False
Output: IdList 1: function BF.Query(x)
1: function MC-ODXT.Search Client
Client 2: Select hash functions {ℎ , . . . , ℎ } for BF indices
2: Set ←(strap,1) 1
3: Initialise empty index set BFIdxSet
3: = UpdateCnt[w1] 4: for ∈ { , . . ., } do
4: Initialise stokenList to an empty list 1
5: Initialise xtokenList , · · · , xtokenList to empty lists 5: bfidx ← ℎ (x)
6: for = 1 to do 1 6: BFIdxSet = BFIdxSet ∪ {bfidx }
7: stokenList = stokenList ∪ {bxtrap } 7: ShufÒe elements in BFIdxSet
8: for = 2 to do 8: Send BFIdxSet to the server
( , ||)
9: Set xtoken =bxtrap 1 Server
, 9: for Each idx ∈ BFIdxSet do
10: Set xtokenList =xtokenList ∪xtoken
, 10: if BF[idx] ≠ 1 then
11: Randomlypermutethetuple-entries of xtokenList 11: Return False
12: Send (stokenList,xtokenList , · · · ,xtokenList )
Server 1 12: Return True
13: Uponreceiving env from client, verify env; if verification fails, return ⊥; otherwise decrypt
env WemodifythisbasicBFconstructiontoallowstoringredundant
14: Parse EDB = (TSet,XSet)
15: Initialise sEOpList to an empty list elements (total ℓ indices generated from ℓ hash functions) to be
16: for = 1 to stokenList. do stored for each xtag (corresponding to each (w,id) pair). During a
17: Set cnt = 1
18: Set stag ← (stokenList[])1/ query, BF accesses only a random subset of size of these ℓ indices.
19: Set (sval, ) = TSet[stag ] Such that the server “sees” that each time different indices are
20: for = 2 to do beingaccessedandcannotcorrelatewiththerecordedinformation.
21: Set xtoken =xtokenList []
,
22: Computextag = (xtoken ) / Wecall this redundant element-based Bloom filter construction
, ,
23: If XSet[xtag ] == 1, then set cnt = cnt + 1
, as a Redundant Bloom Filter (RBF). The updated RBF.Insert and
24: Set sEOpList = sEOpList ∪ {(,sval,cnt )} RBF.QueryroutinesareprovidedinAlgorithm16andAlgorithm17
25: Sent sEOpList to client
Client respectively.
26: Initialise IdList to an empty list
27: for ℓ = 1 to sEOpList. do
28: Let (, sval, cnt ) = sEOpList[ℓ] Algorithm16RedundantBloomFilterInsert
29: Recover (id ||op ) = sval ⊕ ℓ Input: Input parameters: x - element to be inserted into RBF
30: If op is ADD and cnt = then set IdList = IdList \ {id } Output: Output parameters:
31: Output IdList 1: function RBF.Insert(x)
Gate-keeper
2: Select ℓ hash functions {ℎ1, . . .,ℎℓ } for RBF indices
C REDUNDANTBLOOMFILTER 3: Initialise empty index set RIdxSet
4: for ← 1 to ℓ do
5: rbfidx ←ℎ (x)
Theplain Bloom filter (denoted by BF) is a probabilistic data struc-
6: RIdxSet = RIdxSet ∪ {rbfidx }
ture suitable for membership checking within a set encoded in the 7: ShufÒe elements in RIdxSet
BF. At a high level, to index an element (or insert), a BF uses 8: Send RIdxSet to the server
Server
different hash functions to obtain addresses, which are set to 1. 9: for Each idx ∈ RIdxSet do
Duringmembershipcheck(orlook-up), indicesareobtainedfrom 10: Set RBF[idx] = 1
the queried element and checked for 1’s. These BF insertion and
look-up/queryroutinesareoutlinedinAlgorithm14andAlgorithm Algorithm17RedundantBloomFilterQuery
15 respectively. Input: Input parameters: x - element to be queried in RBF
Note that if we directly plug BF into MC-ODXT, replacing the Output: Output parameters: True/False
XSet insertion with BF.Insert and XSet retrieval with BF.Query, 1: function RBF.Query(x)
the construction essentially works the same. However, the leak- Client
2: Select hash functions {ℎ1, . . .,ℎ } for RBF indices
age is not mitigated as the bfidx s (or xtags in the context of SSE) 3: Initialise empty index set RIdxSet
4: for ∈ {1, . . ., } do
generated during BF query are deterministically generated using
5: rbfidx ← ℎ (x)
hash functions. Hence, the server still can associate a w using the 6: RIdxSet = RIdxSet ∪ {rbfidx }
observed BF (or XSet) addresses. 7: ShufÒe elements in RIdxSet
8: Send RIdxSet to the server
Server
9: for Each idx ∈ RIdxSet do
Algorithm14BloomFilterInsert 10: if RBF[idx] ≠ 1 then
11: Return False
Input: Input parameters: x - element to be inserted into BF 12: Return True
Output: Output parameters:
1: function BF.Insert(x)
Gate-keeper C.0.1 RBFOverhead. In RBF, the server sets ℓ locations, and ac-
2: Select hash functions {ℎ1, . . .,ℎ } for BF indices
3: Initialise empty index set BFIdxSet cesses locations during query, where ℓ > . The value of needs
4: for ← 1 to do to be chosen suitably to have negligible false positive probability
5: bfidx ←ℎ (x)

6: BFIdxSet = BFIdxSet ∪ {bfidx }
7: ShufÒe elements in BFIdxSet (similar to normal BF) without blowing up storage.
8: Send BFIdxSet to the server Storage overhead. A conventional BF requires
Server ∑︁
9: for Each idx ∈ BFIdxSet do · |DB(w)|
10: Set BF[idx] = 1 w∈Δ
storage for BF with hashes. Here, we have hashes during 100
insert, and ℓ hashes during queries. Hence, the storage requirement ] 80 = 8
of RBF is 60
∑︁ [
ℓ · |DB(w)| 40
w∈Δ 20
. 5 10 15 20 25 30 35 40 45 50
RBFstorageoverheadis ℓ times(greaterthanoneasℓ > )than ℓ
BFforthesamedatabase.
Communicationoverhead.AnRBFsends indicesforasingle Figure11:GrowthoftheRBFaccessupperboundwithredunelement while inserting into and querying on BF. Thus, the com- dancy. The look-up indexing hashes were fixed at random
munication overhead can be expressed as(1) for each inserted 8-sized subset.
element (from (), as remains constant for a particular database). For a complete query = w ∧ ... ∧ w , the query overhead
1
can be expressed as follows. MaximumhowmanyRBFaccessdoestheadversarialserver needs to
· ∑︁ |DB(w )| “see” for the same (w,id) pair from a benign client’s queries before it
w∈{w ,...,w } 1 can figure out that the same (w,id) pair is being accessed?
## 2 Asitturnsout,thisproblemisidenticaltothewell-knowncoupon
WithRBF,thecommunicationoverheadduringtheinsertion of collector’s problem with coupons collected in batches. When transa single element is (1) (from (ℓ)) as ℓ remains constant for a lated to the coupon collector’s problem, the problem statement can
database. For a conjunctive query of the form = w ∧ ... ∧ w , be expressed in the following way.
1
the communication overhead can be estimated as follows, Maximumhowmanydrawsarenecessarytocollectallℓ coupons if
· ∑︁ |DB(w1)| in each draw uniformly random-subset of the ℓ coupons is collected
w∈{w ,...,w } with replacement?
## 2 Theclosed-formexpressionofthisupperboundcanbeexpressed
since indices are used for query (instead of all ℓ indices). Clearly, as below.
the communication overhead of RBF is ℓ times than BF (greater
    
than one as ℓ > ). However, if the same values are chosen for ℓ ℓ
RBFandBF,thecommunicationoverheadessentially remains the [ ] = ∑︁(−1)+1 · ℓ · (1)
(ℓ−)
sameforbothRBFandBFduringlook-up. =1 1−
(ℓ)

C.1 Security Analysis of RBF The complete proof can be found in [33] (albeit in a slightly
different form). We plot the growth of this upper bound [ ]
Theredundantaccess in RBF aims to mitigate the cross-term leakageinapracticalyetfinitemanner.Weanalysetheeffectofrepeated with the number of indexing hashes ℓ in Figure 11, which shows
RBF look-ups to evaluate the leakage profile of RBF. Since RBF the monotonically increasing behaviour. The parameter remains
relies on plain redundancyratherthanstandardcryptographichard- constant to maintain the same desired false positive probability of
ness assumptions, the analysis primarily assesses the advantage a BF. This bound grows slower than the exponential that is ideally
of RBF compared to BF (for which the CrossAttack of Section required to eliminate the access pattern completely in practice. We
3 in the main manuscript works) with respect to the redundancy argue that if practical client search policies are formed based on
parameters ℓ and. the query semantics and the upper bound, this approach prevents
Recall from Section 4.2 of the main manuscript that RBF uses ℓ cross-term–based leakage.
hashes to index a value during insertion, while it uses a random Inreality, a client’s queries are concentrated on a particular topic,
-subset of these ℓ hashes during look-up to hide the access pattern. andaclient typically issues only a limited number of queries in a
Since it requires more number of RBF accesses to deterministically searchsession.Therefore,theessentialrequirementofencountering
relate a specific (w,id) pair to the ℓ indices in RBF, compared to a the same (w,id) pair across these queries is limited to a query
single on in BF, in practice it results in less leakage. session only. It is unlikely that a client would issue more queries
than the upper bound [ ] in a session, as plotted in Figure 11.
Previousworks[1,22]exploredthatredundancy-basedapproaches
wouldrequire a linear amount of storage on the client side to elimi- Thus, the administrator can enforce the search policy such that a
client cannot issue more queries than the upper bound [ ]. We
nate access pattern leakage (which indicates that pattern leakage
maynotbepossibletoeliminateinpractice).Hence,RBFfocuseson state the following assumption to reflect the RBF’s influence in
reducing the attack probability compared to a plain BF up to a limit. Nomossecurity analysis.
Weargueinthisdiscussionthat,inpractice,itisnotfeasibleforthe Assumption. Given an RBF with ℓ hashes for insertion and a uniadversary to build the required (w,id)–xtag association within a formly random-subset of these ℓ hashes for look-up, number of
reasonable time. Hence, this brings a notion of access upper-bound RBFlook-upsforthesame (w,id) pair are indistinguishable from
in RBF beyond which the advantage would reduce to a traditional a random RBF element (corresponding to a random (w,id) pair)
BF. Analysing this RBF access upper bound is equivalent to ad- look-up using a uniformly random-subset of these ℓ hashes up to
dressing the following question. [ ] accesses, where < [ ].

Tokenised Multi-client Provisioning for Dynamic Searchable Encryption with Forward and Backward Privacy ASIACCS’24,July1–5,2024, Singapore, Singapore
Remarks. The current analysis of access bound assumes the server out if two sets of xtags are “related” rather than knowing that
woulddefinitely be able to figure out after the expected number of these are from exactly the same (w,id) pair. In that case, a different
queries given by the closed-form expression in Equation (1). In that analysis approach is necessary. However, the exact-match base
case, the problem is the same as the Coupon collector’s problem, analysissufÏcestoprovideanin-depthoverviewoftheRBFsecurity,
as stated above and followed in the abovementioned analysis. In and we resorted to the upper-bound-based analysis to choose RBF
case of an approximation or relatedness measure is considered in parameters and simplify the analysis, compared to a “relation”the attack process instead of an exact match for xtags to figure based analysis which we leave for as an extension of this work.
