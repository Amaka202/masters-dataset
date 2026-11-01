"""Training-only consolidation proposals; source and ledger text stay inert."""
import argparse
from collections import Counter, defaultdict
import csv
import io
from itertools import combinations
import json

import CATEGORY_AUDIT as audit


PLAN = 'CATEGORY_AUDIT_CONSOLIDATION_PLAN.json'
REVIEW_BATCHES = ('CATEGORY_AUDIT_CONSOLIDATION_BATCH_001.json',
                  'CATEGORY_AUDIT_CONSOLIDATION_BATCH_002.json',
                  'CATEGORY_AUDIT_CONSOLIDATION_BATCH_003.json',
                  'CATEGORY_AUDIT_CONSOLIDATION_BATCH_004.json',
                  'CATEGORY_AUDIT_CONSOLIDATION_BATCH_005.json',
                  'CATEGORY_AUDIT_CONSOLIDATION_BATCH_006.json',
                  'CATEGORY_AUDIT_CONSOLIDATION_BATCH_007.json',
                  'CATEGORY_AUDIT_CONSOLIDATION_BATCH_008.json',
                  'CATEGORY_AUDIT_CONSOLIDATION_BATCH_009.json',
                  'CATEGORY_AUDIT_CONSOLIDATION_BATCH_010.json',
                  'CATEGORY_AUDIT_CONSOLIDATION_BATCH_011.json',
                  'CATEGORY_AUDIT_CONSOLIDATION_BATCH_012.json',
                  'CATEGORY_AUDIT_CONSOLIDATION_BATCH_013.json',
                  'CATEGORY_AUDIT_CONSOLIDATION_BATCH_014.json',
                  'CATEGORY_AUDIT_CONSOLIDATION_BATCH_015.json',
                  'CATEGORY_AUDIT_CONSOLIDATION_BATCH_016.json',
                  'CATEGORY_AUDIT_CONSOLIDATION_BATCH_017.json',
                  'CATEGORY_AUDIT_CONSOLIDATION_BATCH_018.json',
                  'CATEGORY_AUDIT_CONSOLIDATION_BATCH_019.json',
                  'CATEGORY_AUDIT_CONSOLIDATION_BATCH_020.json',
                  'CATEGORY_AUDIT_CONSOLIDATION_BATCH_021.json',
                  'CATEGORY_AUDIT_CONSOLIDATION_BATCH_022.json',
                  'CATEGORY_AUDIT_CONSOLIDATION_BATCH_023.json',
                  'CATEGORY_AUDIT_CONSOLIDATION_BATCH_024.json',
                  'CATEGORY_AUDIT_CONSOLIDATION_BATCH_025.json',
                  'CATEGORY_AUDIT_CONSOLIDATION_BATCH_026.json',
                  'CATEGORY_AUDIT_CONSOLIDATION_BATCH_027.json',
                  'CATEGORY_AUDIT_CONSOLIDATION_BATCH_028.json',
                  'CATEGORY_AUDIT_CONSOLIDATION_BATCH_029.json',
                  'CATEGORY_AUDIT_CONSOLIDATION_BATCH_030.json',
                  'CATEGORY_AUDIT_CONSOLIDATION_BATCH_031.json',
                  'CATEGORY_AUDIT_CONSOLIDATION_BATCH_032.json',
                  'CATEGORY_AUDIT_CONSOLIDATION_BATCH_033.json',
                  'CATEGORY_AUDIT_CONSOLIDATION_BATCH_034.json',
                  'CATEGORY_AUDIT_CONSOLIDATION_BATCH_035.json',
                  'CATEGORY_AUDIT_CONSOLIDATION_BATCH_036.json',
                  'CATEGORY_AUDIT_CONSOLIDATION_BATCH_037.json',
                  'CATEGORY_AUDIT_CONSOLIDATION_BATCH_038.json',
                  'CATEGORY_AUDIT_CONSOLIDATION_BATCH_039.json',
                  'CATEGORY_AUDIT_CONSOLIDATION_BATCH_040.json',
                  'CATEGORY_AUDIT_CONSOLIDATION_BATCH_041.json',
                  'CATEGORY_AUDIT_CONSOLIDATION_BATCH_042.json',
                  'CATEGORY_AUDIT_CONSOLIDATION_BATCH_043.json',
                  'CATEGORY_AUDIT_CONSOLIDATION_BATCH_044.json',
                  'CATEGORY_AUDIT_CONSOLIDATION_BATCH_045.json',
                  'CATEGORY_AUDIT_CONSOLIDATION_BATCH_046.json',
                  'CATEGORY_AUDIT_CONSOLIDATION_BATCH_047.json',
                  'CATEGORY_AUDIT_CONSOLIDATION_BATCH_048.json',
                  'CATEGORY_AUDIT_CONSOLIDATION_BATCH_049.json',
                  'CATEGORY_AUDIT_CONSOLIDATION_BATCH_050.json',
                  'CATEGORY_AUDIT_CONSOLIDATION_BATCH_051.json',
                  'CATEGORY_AUDIT_CONSOLIDATION_BATCH_052.json',
                  'CATEGORY_AUDIT_CONSOLIDATION_BATCH_053.json',
                  'CATEGORY_AUDIT_CONSOLIDATION_BATCH_054_CORRECTED.json',
                  'CATEGORY_AUDIT_CONSOLIDATION_BATCH_055.json',
                  'CATEGORY_AUDIT_CONSOLIDATION_BATCH_056.json',
                  'CATEGORY_AUDIT_CONSOLIDATION_BATCH_057.json',
                  'CATEGORY_AUDIT_CONSOLIDATION_BATCH_058.json',
                  'CATEGORY_AUDIT_CONSOLIDATION_BATCH_059.json')
OUTPUTS = {
    'crosswalk': 'CATEGORY_AUDIT_CONSOLIDATION_CROSSWALK.json',
    'queue': 'CATEGORY_AUDIT_CONSOLIDATION_REVIEW_QUEUE.jsonl',
    'dependence': 'CATEGORY_AUDIT_CONSOLIDATION_DEPENDENCE.json',
    'counts': 'CATEGORY_AUDIT_CONSOLIDATION_COUNTS.csv',
    'report': 'CATEGORY_AUDIT_CONSOLIDATION_REPORT.md',
    'manifest': 'CATEGORY_AUDIT_CONSOLIDATION_MANIFEST.json',
    'reviews': 'CATEGORY_AUDIT_CONSOLIDATION_CASE_REVIEWS.json',
}
STATUSES = ('assistant_supported', 'assistant_ambiguous', 'assistant_proposed_exclusion')
DISCOVERY_PREFIX_EVENTS = 744
DISCOVERY_PREFIX_SHA256 = 'e3f957277307f3bac985d041c3406cde8b00478842921860352a87389b1077d4'
# Supplemental pins are separate from the immutable released-input lock. These
# digests were recorded when the training evidence was collected.
SUPPLEMENTAL_PINS = {
    'CATEGORY_AUDIT_EVIDENCE_019_ENUM_TEMPLATE.txt': 'f47c28c06937f64170129f75ca8a4c63d609b65deca4032039e9948a54983d98',
    'CATEGORY_AUDIT_EVIDENCE_021_CONTEXT.json': '1f150f0e0247e26f812344ea9a2e353af3fd7483c6e9b6f49ab4dfe88e3c2fea',
    'CATEGORY_AUDIT_EVIDENCE_022_CONTEXT.json': '7108d5a1d03015dc0c301a7ec2f092d9e348c8373fd6f6d2ac611c33b12d7cfe',
    'CATEGORY_AUDIT_EVIDENCE_023_CONTEXT.json': '6d9584cf0184899a2ea954b1091f58994d5b39c162b87ed99f7eb856aaf0a9b3',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_001.json': '8b025086e85bae1dffa40cd776f553c8f95b49591d932e369d2b43cc231530a8',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_002.json': '8aa4103ce89005694c2884f46ba52ec0aa26826c69ddbd1fd7975851968f380b',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_002_CALLER.json': 'd5fa05ab08fb29a57504af44114d784e37a9b534e67dba35fe2a9eb9b93106a3',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_003.json': '892abaf17617b669f093ff9fdcbcecfd2f7f8b5ce805a641d6a4dffe30631e1d',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_004.json': '18acb528b7cee3fafa866bfaafc64ae807d82b4bdb01f420ada5e1bf6a60a492',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_005.json': 'e249902c1f1b390e702b05957cbbc775b3e1b849eda85feae7154e7d20ae8f3f',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_005_GRAMMARS.json': '68db664a38b4691007d496d12c2f3dae0fbdcc64ec157dda56e39711ce79f94d',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_006.json': 'a92e0507e0a78dcb7fe540cfef718c07386d3c19004b32c65f26cd4503cd99ee',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_007.json': '739e4037d19e05f474816d032472226fe2e005ba5e4fff804d235024877ff8fb',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_008.json': 'b9e49558ce18f9267433ee2551ed001871382039512dc59fba5ffac3cb755baa',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_008_HELPERS.json': '9b43c3c8b037b75398eafae62236be6394c2599e9e59ea20670ab5f6178775b7',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_008_CAST_HELPER.json': '0b1700597551534daaa0e5a71223bab951943cc7fd23ccf1e3dd6797d6ba6645',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_009.json': 'f329189b9478c00d354f478215f30297e595ae04af6962eaef17b91e07c8baca',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_009_HELPERS.json': '93f57b2f080ad9ef814a75dd5d866ff3c1ab0febd8e4eb841df036dc3e9eefb2',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_010.json': '8ddfd4a7f830e596df885a721c381beb6ef0b0c00c53019ffe1b5e5d7fbb8a5d',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_011.json': '3df64f8f44fd989803ab4ba2ce0c5b9fe99d1854491f75ac7e30d1656048bd37',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_012.json': 'cd9b53f55329cc85e0561d075178820e85f2fbe6cd58ded40c607182e70b5da2',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_014.json': '77485ed79e372051c8d4b0955937b24deee78fa0a82aa140b048e1c4a127f977',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_015.json': '7f8b2c6b29b6185c8c44e57bd4ad07630f8b2eb1d42fc73e819741caeee1ecd7',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_015_FRAMEWORK.json': '3c0a3546a3d8df081202d115b89de636115d474f3a82d7d92de26ccb61c1a99e',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_016.json': 'f48191a4227faff6aba6fc3194c8ff8f4d2eb02dd3b654fa17545872e230403e',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_016_CONTRACTS.json': '87c053618b3a822fe9b5ebd7d5d59f6fae8ed1f09dad4cf5e3dee464b6b29278',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_016_TOKENIZERS.json': '480e402ce45077136387885278c7f87530e399274527dc58661df83411f7d518',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_017_GIT.json': '7c1c968948efd1a36eb8a1db7a975b64f312d7e476990496ee0d3d302863e830',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_018.json': '06042beef14765eaef9902fc4eb94aeec3657846bcac81a4467aa2595188065a',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_018_POLICY.json': 'ec4392e00e37b8e5941dccd4222eefa925d3753e1f46abf212de0ffccbf4b1da',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_018_ADVISORIES.json': '38c76d8fcad31ef14c2e2571d0e7f0a4778ada1cb34c834eee181224487f2c2f',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_019.json': '165f8df6d74c5e8efebae48ce6da5922507d1d196f45ea3760e05b679ad1b170',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_019_RUNTIME.json': '5b6df00e394bf71acac94e1347debdaa8aadd8bb36f53c5f41ca2c711464f1f4',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_019_CONTRACTS.json': 'df17ec119f3f01562fca95ea2f815c5cefab1e96fa6d9ad891b8e941f52010e9',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_019_FACTS.json': '00b59b9f166d2ea87620bb566d5c7b1d5f300b9452e1eb86e924ce0a99c8fe0d',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_019_ISSUES.json': '19311fe5bfb6c42fd9798b1b41ff62b3b4f8d3c9e44bde8e5bfcf0897fa4cc12',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_020.json': 'c8a400168464d6f5a0a35a5aa9a2d86568d5a88540f99f47573e90b1ac05fa4d',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_020_ADVISORIES.json': '47be06709cee7e59f2986006ba72323a41c5b36ca1c2c23e307684d699616292',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_020_RUNTIME.json': '72166ca7549e83b021c507a66068c9f7bd96001a631afd2824fc29b7c15e00c7',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_020_LIFECYCLE.json': 'b53b455f8d55f77188fd5b69990584ab48297c82822f963101dae7dcdc961094',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_022.json': 'a26133a1fda0cd1594f4b54b97b9678b91429513db9abaffcbdf2a29d9748bfc',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_022_DELIVERY.json': 'e19243f9c2c258181a67d660299090546e3aa22ee0b783e07e6fec285440fb45',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_022_STORAGE.json': 'db80340fdf86d46a528d507af6b913e74a4d92a392887ecbea40e56fb87107be',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_022_ADVISORIES.json': '997c3e7ccffe5260d3aed4d17cecb7f089a759987fda37296755a6c24ca8cb87',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_022_POLICY.json': 'b8617d57846197b4d275e414eeb62f1ab2fa394a94e3110d412c29c88ce95590',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_023.json': '42ff7f5ebfa9e01488a7f465383c2c3bb1fce9b503d430ebd61438fbde72c1e4',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_023_DELIVERY.json': '4b81328339765f31c97d8df56336e3ba2908b5a7e5e2ab005cde70600eb65918',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_023_CONTRACTS.json': '538de89512cfd8b5b09134e8c6696c41b1fabd309a474665d2bc7b5ed57c98b0',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_024.json': 'e5b907ca61e5422122cd070281b24bc8c6fb994282dcb12a9c740fa650ec93ec',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_024_DELIVERY.json': 'c7c1731e04c6ab482c427313e3337b16d28c767c0cb1a62cc85be1830a8d2ffc',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_024_PEERS.json': 'b4a05c3287da867f77c1d302016e5286700b203e2fef3faa86c3b4f7006ba13e',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_025.json': '3d51bb5070cbf54194ba53296b65c58bdda01d948e0052b381500518bd315692',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_025_PEERS.json': '466a49dc6029cf8449e374ea71d8e594d28fa078d1d980ea5038ab858fa672c7',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_025_RUNTIME.json': '11eda7246670dfd5838b4c6cca6076c561b792926d42eaa9378a23513b07fb90',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_025_DELIVERY.json': 'a677644d078ed63c737f7edc22e886ffa7223f439e938936e77361673efacf0a',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_025_ACTIONS.json': '056f356428cae0ceaf814808a225b1cc773d860a4ee412444de017fd80c179eb',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_025_MESSAGES.json': 'cd366bb6256290ad127da412171e4b0f53d2acfd21e83d86f9febc0af828dcf7',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_026.json': '35bda94234ff3242f27763f530c8deb5191e0420aa63ff6f41c1c6fdcc1fe19c',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_026_PEERS.json': '080a85d0df873c1e9d994714cd709d4712b0a6250731071ddae93fca73436961',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_026_RUNTIME.json': '5ef27926a842fe5e306dab29fb8dbe71908a0f66f9b8f05437e56a88586faeec',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_026_DELIVERY.json': '52e267d0e467b057a2b378a053de0e108f0f237610588ca4d38d6390eb14a1d0',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_027.json': '0cf271f33841bedf22b9de17592ea1835cbb017753e0f32cfc2885982c8284ff',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_027_PEERS.json': '4998fec9842d68cb17a456f9df0d5773c70ccd594f5e8101cae132d22c4b0b7c',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_027_CONTRACTS.json': 'a786cb7cd989805af98c65a985a733d697a973f20f01ac89f6eb62ee8dfac705',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_027_BACKEND.json': '7afb56a3867f0452f7a105d8431c2c829fa28ed7368c33ccde71e8fa4fa1b443',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_028.json': '2f32e42c5e84dfb10e84afcadd28562a8dd8d5cdce25a25d15354ed6b60a3e87',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_028_PEERS.json': 'f8a0e967e51bfc46ac587ccdb123d88807d5f074c58f92c1970d941e989bcf35',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_028_DELIVERY.json': '60c38916bde57133ffea256807c0ed1ab30c864a3768d13b14d92b142b762c89',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_029.json': '91205dc9547b0d61195ee83e4d04cb646d08fdb1549046c8aa74d90e84f7b49d',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_029_PEERS.json': '69ba0a70095c60d9e054407dad479cde2c4642efae9297cd12ae99435a1ac1cf',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_029_DELIVERY.json': '7b9b5f839d3545663eb0e61109592d136b108f3a5f4200759d0bba43a892a58f',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_029_ROUTES.json': '94e01714a93673a98ce1c110387b14dbe0770d68e9e9649ff9f7bfd021126b84',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_030_SEARCH.json': '7522ba145a28007d09d1115e1a0a85bb9c516eae12fe5ce41552bf07899bcb4a',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_030_CONTEXT.json': '17c60a3d1eb4e95fa85b1424fb59300c7726a20c2df70c27b5f8022be8b2f5db',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_030_PEERS.json': '29471ac62222c20626ab70f31b4a626a9753ea04b7fc2f0c7b38ba7af2a93717',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_030_DELIVERY.json': '9788c1da138f00848060499eede949d7492ce01cdfffe90850ee093afa166218',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_030_CONTRACTS.json': '3a3a4018e251d7a1762264aa1d7c677458656dd1fd25f703aa5948de3f055361',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_030_ROUTING.json': '1231c21a83b4748c56b55be7ab9b360cd27f59797aaf136859e6dae1a7b11f0f',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_031_CONTEXT.json': '89a344d9f3092885fe2e5e0c0a72cf4d2cc1d593378fb416057b65fdc8d868a8',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_031_PEERS.json': '658f7edaf3fbf221c86f90ebdf98463252d576d4446b5c66dd4edd9c847fabe3',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_031_SEARCH.json': '5b6528aa33e352351037736fb8735c9b11dbc17a874d56766a91d322767bc47c',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_031_CONTRACTS.json': 'bf51c82a08327dae5dd1b10a1141eefad71b7dcbb318a8f1360ecbed2729d65b',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_031_LINEAGE.json': '44bf2effa2bbf250d52badc0c0d42c338e0e029004fb4860c5058fe5d6d8616b',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_032_CONTEXT.json': '8a6fcd2dbf8b63f7b2e18734bfb6fbfbe349acae1e9ef2e52395a341d9432fef',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_032_PEERS.json': 'e7296e4e45fdb3392565e5145e657a6e0d9526ec4a223e3321b4c72abe78cf4c',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_032_CONTRACTS.json': '850399d1e64cbb875e514babf9c75f9bcf48e6b6c8f7a356f7063992677f6527',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_032_DELIVERY.json': '77516f384050aa1fa0aca8570bb9d0b4f747c2c9562442910bbbf6d775116783',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_033_CONTEXT.json': 'b081c1187a36cb8f7bd0ecee24d754cd4c199eda505289011d00b7eb5758c636',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_033_PEERS.json': 'b48b6918d3b1bdcfce569f904cd4a0e7dfe5c7471888988cb68a590d989eab02',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_033_CONTRACTS.json': '5d12faa9a4084669e7d61e72d0421dce2ef273adb39cc8ce05bc919454752300',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_033_RUNTIME.json': 'a762cc339d26aac1abec014f47308792cd7366d9f20c705669bb475e1d755708',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_034_CONTEXT.json': '072d194bf4736f11a0a49d52117244a0655a8444e06b6aca4f6dca534e130556',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_034_PEERS.json': '087f22ac4e8fc622b55c97ef2cd4b46cc23ceac4fcdf00915ce56735328b6f0b',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_034_CONTRACTS.json': 'd1f887e54cbe431b97a83afcf55c9240afcae4ab6c852a32a7138368451bf240',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_034_DELIVERY.json': 'ebfbdbec25baf21ab1e28bf318930d880ee9f9e4a10d470e9dccb3e1c0e0a43e',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_035_CONTEXT.json': '3511f71422f9f209c7bc55c7e9fead30f68692e29fc7a8d75d1654ea8f375a2e',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_035_PEERS.json': 'bb5b4b3a65e54c37c4308f1b4c2e18472241566867751641623f0bf9633af854',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_035_CONTRACTS.json': 'd30d6ac994416cd77b16a6fd05e100a739aa5e757cd61ba1cc173b27b14fa6f1',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_035_DELIVERY.json': '399490eca609404575cd41f9517c7e2dec322112d6de9e153afbbb1d7e69567b',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_036_CONTEXT.json': '71fdb91c5435be00bb57ef9644b9fcc04852af7a79a7a52007df46d56c0da9be',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_036_PEERS.json': '3e9d5a23b17ae19213d7cd29acd0fbe8b939d57fe8337be4ae95c639f84b95e0',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_036_CONTRACTS.json': '410f483d5d7429e7f6ab75a4fd3624bdf0dea2e3a051b9485ba98d4ee54d5e84',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_036_DELIVERY.json': 'a1784ee56e505ee84145238a80652dce3a74cd9f750f8b40f8909ef4a4a685bc',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_036_SESSION.json': '547a066c00508d1c00c0341727e883b683d8499d354906225705ffc8ebdf158a',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_036_ROUTING.json': '0d662c8460b26d4cd9766670832efc57a46498fd73dc165058c215d226a91989',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_036_CONFIG.json': '96355b72feed7e2b5e80778c195671db6586364e71ae26f2c4c49f275a51f799',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_037_CONTEXT.json': 'ecaf03bcc4cad087b1342c4a3d9a618e71b573dfbb0bca1286dd710e3d80be67',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_037_PEERS.json': '82864cdb978d8544e7167989425e559c6c52486f572dfdc63fd5cbe7bee55178',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_037_CONTRACTS.json': '4b026368da84e3ce448010a9719a634d47e23aca52aaa995c8784eafe73c9d06',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_038_CONTEXT.json': '98cf0e8877dcd652080ff8cdec65fd40dd14ae3b00fda1ea089314d9bd39c735',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_038_PEERS.json': '49b8341f772057164b0b389d7728345b63c45d89e041ae86ef79a5ad553c8769',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_038_CONTRACTS.json': '7eadf06f4e37f108a1a29935afe0db6626d8878b20d89d9303c2602285eaf970',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_038_DELIVERY.json': '811ea57702d602d280ef6cc927a045cf1bfa2cfda36e8455bae92d0a1f5a35b8',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_039_CONTEXT.json': '64b268afdec94ad270d49a387b9022630a999ff9556d76cb63340e40b74e0ee3',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_039_PEERS.json': 'b3396be6c950c98ad6ea36ed1cd0d846c9f71e8e3b4c82cae174bdd5f17309e0',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_039_CONTRACTS.json': 'a576437e0bdae61df1931fa8d66643d1d9e240a30c9f93f57cf5029140f59b1c',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_040_CONTEXT.json': '49b20c825eb11397ddb8b4f3b55158b316998f319fb1d418391642e38dd8b6c4',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_040_PEERS.json': '039fe86175723ce0f92b6f7caf0b632a36f6f096dca00d599e1110f4b5853c12',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_040_CONTRACTS.json': '153eb561db818eacfa44c647be13f4b4a11f5ef08b7e70b878f2bc24b8558b1c',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_040_RFC.json': 'ccb662456a61d41c5e906c446a4d7bc41a5e1a9634a3a1de095ac5ee374c39e0',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_041_CONTEXT.json': '5582672c13957e15e6481d957dfa541cf5b904975c74f6bb8fff740140bd6d2a',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_041_PEERS.json': 'a04191fc261d88a5b0dfb98cfa9b99c6c8c2cb36d0da8c10377380d73e7b5d2a',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_041_DELIVERY.json': '6e6c68f8e04052089b9fe786333cfc1ce63fd04bcdf4af4eacb4cabfe132dfe8',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_041_CONTRACTS.json': '317f6a6d94f292566002859b6f7075349798b84ced076504047efdc6e27a13ec',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_042_CONTEXT.json': 'ab70c395666ffd12e654e1c7df049ff5bceac49995313ce66aa32b313de287ac',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_042_PEERS.json': '10df8f480d96fbb6dd9d614bfd8504f66513520e6859e857353cfcd089021c84',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_042_CONTRACTS.json': '3b8b8227c545195759c7a3459b099fa38f85f12dcbed8669fd01a4e66f6028bc',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_043_CONTEXT.json': 'b3ce08114d9b364dad6774aa66f28a4c13c243249f63a644e087ad4d276f8640',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_043_PEERS.json': '741a70fe9f44f5a50599b0cf82f8d2b03e4aefdf0bc70cd0d515aaf32a3b1f3f',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_043_CONTRACTS.json': '200ef7182f7826813cad5b0efd38736d3a1b92c2cf604b5941237e5b460231b2',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_044_CONTEXT.json': '5c19136aebce68ab402afa5b30fe0c06164646a991576bd3f33b2ab86508245a',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_044_PEERS.json': 'c207f64f8790565afa3013e211e750a9d20e59ec578a3f2dabda5bcbca3b949e',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_044_CONTRACTS.json': 'e997ac7a9f77bbb8d224d8aeb74c51d071f71b0b5574adced5eb810be923365b',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_044_RUNTIME.json': '628a3b95583ebc7e0c32475bbcb9787388d50fe7f37fa11534cf9590cacf390f',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_045_CONTEXT.json': '3e0c374fc8fccfcb4191f08f6a1b43893910e14e80c6490af4c0bdca46eac22b',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_045_PEERS.json': '4f6fb0aedaf3acd1b3ae7f7f5b60eb703d10958ce4d7c801d0623b6146c07a2b',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_045_CONTRACTS.json': 'd2e8365c511e1cc9415caefaac5a9af6167b2f169e605c629b7733aa8befb29d',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_045_DELIVERY.json': 'e277a69343f4a256a161cb59744da159613fc643fac2422aa991a613f0700c94',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_046_CONTEXT.json': '5f3a778d497ea1c8481ce7145d7730408f234f37558cbb7054a9ad63a3758458',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_046_PEERS.json': 'f7d749d856758a31f989efe4e7a9bce567d76ab9f761326ee0289acae1ee2797',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_046_CONTRACTS.json': 'dec9754896b4306c33e2b21f032301452c33b404628d14f330e6bf2fcdc9ea82',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_046_DELIVERY.json': '56e25c06716fe91d3c640cec5efa5c1540168fc942e3133b57933bf4a3caf4e7',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_047_CONTEXT.json': '0052da0222df744fac4c4955e6d21d5fc5fff00dfad7e17bb891faeaf5147c4e',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_047_PEERS.json': 'b020e31ae6e687cb10222848270f0915b9fd15de0a1ed89c01c505b76c756bc0',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_047_CONTRACTS.json': 'bd3a5f11d52f5547e50183cc1fbf80bed6b379c5fc6fd636c4d2ae446168041b',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_047_DELIVERY.json': '95e3271c7bca3788727b68baaf7659d3ddad9c17c7e5f009d769501f98ec4910',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_048_CONTEXT.json': '4a413a6029537a4fa483eb7c2a11e6c180eef3c1233a80b0e98e3ec218443934',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_048_PEERS.json': '623c7c14693bbb0541ff6efc833921d768d7ed858372baaaa213dd39a5c6a7e4',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_048_CONTRACTS.json': '489ab1a379a4a11bd6273aa6f3071d5efcc27d89099043459a1552f484be14b7',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_049_CONTEXT.json': 'a5ac6a52fe9fccd6221687dc039566e8a55ba6b8c2ab1b77c7bb63b3b22f6bf4',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_049_PEERS.json': '9d3231deac9e74692c13e02ee46f4ceac93274dd7222251a3b6ba77dcb720f71',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_049_CONTRACTS.json': 'e6ec381af692970ea9df7022b480fccec3efcf1ee18f9e3352c5f6c8a30d4bf6',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_049_DELIVERY.json': '65b91080b12bc3709eed9d732dde315d2169e1e50f4a97b59f1fa8d907dfb465',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_049_UI.json': '8f8c1baec7e466d1de47e0036180a43e66ced44f1d4fb601b9d1e2e86bb4c900',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_050_CONTEXT.json': 'e34b52f8c79684e70d194e51eee2c91ddd14885479591460c177718f24f31cfc',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_050_PEERS.json': '0d3ecf4d554cda06c9ca434f11d8c2995d9d0bcbfb00398b5c30fa83b4e4a65f',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_050_CONTRACTS.json': '819b8a8924654eee5e8d8121b853bf05be58438b413bacbc503ae9af0e10563b',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_050_DELIVERY.json': 'd9b707e7997f4efe077892fa36634b2cbc6f385e325212052e6146c38b7dab4d',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_051_CONTEXT.json': 'ffb03e86de72d57234c9404ce9c8c9457764542792218d21ad63ec8cfe48ee20',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_051_PEERS.json': '5d151b34d5224a8e9bc60b69abc88b04b7b6b27948c2f90afb4eca4306f33254',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_051_CONTRACTS.json': '37bb6a72658eec0a777834d9af3fdc46ea7284a79893b448252b2cc65aa17760',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_051_DELIVERY.json': '5b81bed588ad38363940432e47d0af1505819c4924ee47b067e2a4d21faf5ec7',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_052_CONTEXT.json': '7559808f8b9040cbda9e169b19646f5dc4377bd9af5fdfa5d6961b9e7e5995de',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_052_PEERS.json': '238ae1cd81887275b8b6d357b9afc5137fb4bc4780fb02ecd658459132a35607',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_052_CONTRACTS.json': '153d2563e45939133e3ff86b1968f7dc7cd845c06c463b35b7ed0ea345e496f1',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_052_DELIVERY.json': '361e54c7ee76c4e2f9382cbd2174df69becf3516fcc8a50056c765f1945edb8c',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_053_CONTEXT.json': 'e9de630faf537ea404123a9ac1a4ea29a13466cb5da7b4e06fcfa7e1d356798c',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_053_PEERS.json': 'f1d4f9f7b194bb614408e5c91b83540b61bf48b5a45ef83bb3fab1bf6795a625',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_053_CONTRACTS.json': 'ec9ce60e42d10cc493527bb410b87640a4b17e8027a6dd38125411c3e4e11280',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_053_DELIVERY.json': '4af6aa6fad8d0e680b0a27fc42d9993b75bd39f15af25c79a01b005dea765c36',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_054_CONTEXT.json': 'f4c1b02700757f0b2cd55dfb5b722c9f21aed816bef9187669447bae46bbc84d',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_054_PEERS.json': '1a530673fb34fa25d818c8da793f197555623776770ab86970d3219ea983c71d',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_054_CONTRACTS.json': '4a3836afb995f31f6684d7384f76417d970be72fb9b1bdfa638dd5ce97e1e2bd',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_054_DELIVERY.json': '5b1c4a968f6066c49634e02b8269033355ed18d4bd77afa23ed3ecdb3e4b6f3c',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_054_AUTH.json': '31c044de440dfa32c9ac2ba86b3f285cf4929717cc9e3478ecd09b74e374aa7c',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_054_CONTEXT_UNIQUE.json': '310c9f7ce53cfa7d4de7a52ea98ee4d8be1c8e1d9225e6d44d54362fb4a4eba3',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_055_CONTEXT.json': '36630c3c63d015dc70888a6393dc63efd42fe0cc05abf013ee9b53447cbf6998',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_055_PEERS.json': 'b46167c1f7027c835873c58facc39a270bea622b168cf7e16b40e4405131bc46',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_055_PEERS_RELEASED.json': '46a5f277dfd133d9a6fd27c132a61d6aeaa65242fc476afb9798d91947e0736d',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_055_CONTRACTS.json': '343aad3ffe9ca2def0c4187f8bc9d3030b97afbfd9bd3f86678a81d7ea4c7f59',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_055_DELIVERY.json': '81a6ef97270b6f21c836ba9da72d5fa7f521e1ffdd3381528566f2f81dc6e48c',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_056_CONTEXT.json': '49dec674a3a7b9347b8a85abac43d24f8aa8e519e04ce45073bd927291d617aa',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_056_PEERS.json': 'a8815a82d860c505f47ab4d78cd71025605bc31decf5f6365a57a8f670355510',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_056_PEERS_RELEASED.json': '3962f006c6b9b62f48303ab3c072c3d31c327638a8dce9470046af8f2c0099f7',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_056_CONTRACTS.json': '378a4238557a9fedc1235bc5d2af56012aa9eb0e9053a20f7891075a8bc37fc8',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_056_DELIVERY.json': '8569c20cf3749a3051d5a2a7a82eea74e3643e551229d71b25f9f4b580869205',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_057_CONTEXT.json': '962ff5e347536e869e1b4ec315b6c20b957209ef3dc0cf11366939f7a0904308',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_057_PEERS.json': 'ba25886db907b4cdc23a451726cca44d32c77ca28b5d2ccf6c1b9f0ae84913f7',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_057_PEERS_RELEASED.json': '1b399499dfa8579f74382ce3e99181f33fbe9d17fd2c1cafd96bddee0cb2548f',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_057_CONTRACTS.json': 'fe2e4287c0f56dc07752a33489e75dd58f8ce586fdb257b0c736b5774cc33ac5',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_057_DELIVERY.json': '346df96d590c1351f57c4d4fc2fac4e8268dcab039059eef4e560c1ffc343cc3',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_058_CONTEXT.json': '8bba20749f701ef8e707cb5422701f15e48c3bc12699edd46750f679fa9b3ea0',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_058_PEERS.json': '57297ecde765b7a1146a003dd5e90c9860035f85b7db221afc882cf7d9a0ae56',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_058_PEERS_RELEASED.json': '45ec81373a45809f523e757173e8581c1e9e66b86c94da6f187249c6abfc1fc6',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_058_CONTRACTS.json': '8f8afa7ed13f70b85968b5d8c0938abd1cb9a621ca9304dc5681983b0c707c92',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_058_TARSAFE_METADATA.json': 'de8422027338ae1e1d2d336b39c3295a81c7332468e312d88387d9ccb0425453',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_058_TARSAFE.json': '5150e57244cfed16e6158214b4bc96bd4841ccdb1d84db2f39f48b223e8d9f83',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_059_CONTEXT.json': '5669c4cf464d929d59fc50731b668d69be95a8884ef969ef7d8e9bc2a09f5698',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_059_PEERS.json': '35e8d06e3216bf5c0cf6e47587f1a1636f4591213c871508cdc02470ee1875aa',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_059_PEERS_RELEASED.json': 'e982f72a1405bf3cdaeeb69d7b7fd5cc8c3618a42458001cc7a92b42541d149e',
    'CATEGORY_AUDIT_CONSOLIDATION_EVIDENCE_059_CONTRACTS.json': '5110fc15b57faa92e545acfe97bec16d695037622aa0e423a102fff3d2ba66af',
}
UNRESOLVED_PAIRED_NEGATIVE_ASSESSMENTS = {
    'unresolved_contract_regression', 'unresolved_contract_failure',
}
BODY_SNAPSHOT_KINDS = {'mutable_issue_body_snapshot', 'mutable_discussion_body_snapshot'}
# Literal retrieval only. Matches/negations are preserved for human interpretation;
# these routes never decide scope, observability, correctness or issue identity.
CUES = {
    'existing_contract_or_feature_policy': ('feature', 'new interface', 'policy change', 'policy revision', 'support expansion', 'old test', 'changed test', 'newly supported'),
    'diagnostic_or_style_contract': ('diagnostic', 'logging-only', 'warning-only', 'style', 'wording', 'presentation', 'formatting'),
    'selected_component_attribution': ('ancillary', 'coordinated', 'refactor', 'migration', 'equivalent', 'selected function', 'selected defect'),
    'paired_negative_and_residual_behavior': ('residual', 'still ', 'not certified', 'not approved', 'not a ', 'unchanged', 'not generally', 'after-code', 'after code', 'negative'),
    'caller_helper_or_input_context': ('caller', 'helper', 'consumer', 'closure', 'external', 'context', 'function-only', 'function only'),
    'runtime_dependency_or_configuration': ('runtime', 'version', 'dependency', 'configuration', 'configured', 'backend', 'platform', 'python2', 'python3', 'python 2', 'python 3'),
    'threat_boundary_and_reachability': ('attacker', 'untrusted', 'lower-trust', 'trust boundary', 'reachability', 'reachable', 'permissions', 'privilege'),
    'issue_alias_backport_and_history': ('alias', 'backport', 'fork', 'same family', 'shared', 'successive', 'independ', 'introduced', 'lineage'),
    'supplemental_evidence_pin_followup': ('must be retained', 'retain/pin', 'retained/pinned', 'needs pinning', 'need pinning', 'pin actual', 'pin the'),
}


def json_text(value):
    return json.dumps(value, indent=2, ensure_ascii=False) + '\n'


def status_counts(ids, latest):
    counts = Counter(latest[pid]['review_status'] for pid in ids)
    return {status: counts[status] for status in STATUSES}


def verify_supplemental_evidence():
    source_count = 0
    for name, expected in SUPPLEMENTAL_PINS.items():
        assert audit.file_sha(audit.ROOT/name) == expected, f'Changed supplemental evidence: {name}'
        if name.endswith('.json'):
            sources = audit.load(name)['sources']
            assert sources, f'Empty supplemental evidence: {name}'
            for source in sources:
                assert audit.sha(source['text']) == source['sha256'], f'Changed retained source: {source.get("url", source.get("path"))}'
                if source.get('source_kind') in BODY_SNAPSHOT_KINDS:
                    assert source.get('api_response_text'), 'Mutable body requires its full API response'
                    assert source.get('collected') and source.get('limitation'), 'Mutable body requires snapshot qualifications'
                if 'api_response_text' in source:
                    assert audit.sha(source['api_response_text']) == source['api_response_sha256'], f'Changed retained API response: {source["url"]}'
                    if source.get('source_kind') in BODY_SNAPSHOT_KINDS:
                        record = json.loads(source['api_response_text'])
                        assert record['body'] == source['text'] and record['updated_at'] == source['updated_at']
                        assert record['url'] == source['url'] and record['html_url'] == source['html_url']
                        assert record['created_at'] == source['created_at']
                        assert record.get('title') == source.get('title')
                        if source.get('source_kind') == 'mutable_issue_body_snapshot':
                            assert source.get('title'), 'Issue body requires its title'
                        if 'labels' in source:
                            assert [label['name'] for label in record['labels']] == source['labels']
            source_count += len(sources)
    return dict(file_sha256=SUPPLEMENTAL_PINS, embedded_source_count=source_count,
                standalone_text_count=sum(name.endswith('.txt') for name in SUPPLEMENTAL_PINS),
                limitation='Hash verification preserves retained text; it does not prove deployed dependencies, complete caller contracts or evidence sufficiency.')


def cue_matches(event):
    fields = {key: event[key] for key in ('reason', 'function_only_observability', 'negative_scope')}
    fields.update({f'open_questions[{i}]': text for i, text in enumerate(event['open_questions'])})
    matches = {}
    for route, markers in CUES.items():
        hits = []
        for field, text in fields.items():
            lower = text.lower()
            for marker in markers:
                position = lower.find(marker)
                if position >= 0:
                    hits.append(dict(field=field, literal_marker=marker,
                                     excerpt=text[max(0, position-70):position+len(marker)+100]))
                    break
        if hits:
            matches[route] = hits
    return matches


def retained_anchor(text, needle):
    assert needle and text.count(needle) == 1, f'Evidence anchor must match exactly once: {needle!r}'
    start = text.index(needle)
    return dict(start_line=text[:start].count('\n')+1,
                end_line=text[:start+len(needle)].count('\n')+1,
                excerpt=needle)


def supplemental_origin(source, train, source_cache):
    """Resolve an archive peer's retained URL only after checking its training proof."""
    if source.get('source_kind') != 'verified_training_peer_text':
        return dict(url=source['url'])
    pid = source['training_case']
    assert pid in train, 'Archive peer must reference a training candidate'
    row = train[pid]
    assert source['repository'] == row['repository'] and source['path'] == row['path'], 'Archive peer identity changed'
    matches = []
    for side in ('before', 'after'):
        key = (pid, side)
        if key not in source_cache:
            source_cache[key] = audit.source(row, side)
        lines, proof = source_cache[key]
        if proof == source['archive_proof'] and ''.join(lines) == source['text']:
            matches.append(side)
    assert len(matches) == 1, 'Archive peer needs an exact retained archive/hash/span/text proof'
    side = matches[0]
    url = row['upstream_snapshots'][side]['url']
    expected = f"https://raw.githubusercontent.com/{source['repository'].removeprefix('github.com/')}/{source['ref']}/{source['path']}"
    assert url == expected and row['upstream_snapshots'][side]['sha256'] == source['sha256'], 'Archive peer ref/hash changed'
    if 'url' in source:
        assert source['url'] == url, 'Archive peer URL changed'
    return dict(url=url, archive_proof=source['archive_proof'], training_case=pid,
                limitation=source['limitation'])


def case_reviews(train, families, events, latest):
    """Validate authored proposals against fixed evidence, never execute source."""
    metadata = {case['case_id']: case for case in audit.load('HAPY_BUG_CASE_METADATA.json')}
    event_for_revision = {(event['pair_id'], event['revision']): event for event in events}
    ledger_lines = (audit.ROOT/'CATEGORY_AUDIT_LEDGER.jsonl').read_bytes().splitlines(keepends=True)
    records, reviewed = [], {}
    source_cache = {}
    # Evidence is immutable within this validation snapshot. Reuse decoded files
    # for their many anchors, but never share a cache across validation calls.
    supplemental_cache = {}
    for name in REVIEW_BATCHES:
        batch = audit.load(name)
        assert batch['schema_version'] == '1' and batch['scope'] == 'training_only'
        assert batch['researcher_status'] == 'pending' and batch['status'] == 'assistant_proposals_not_approved'
        checkpoint = batch['discovery_ledger_checkpoint']
        assert len(ledger_lines) >= checkpoint['events']
        assert audit.sha(b''.join(ledger_lines[:checkpoint['events']])) == checkpoint['sha256'], 'Consolidation source ledger checkpoint changed'
        checkpoint_latest = {event['pair_id']: event for event in events[:checkpoint['events']]}
        selection = batch['selection_rule']
        assert ('repository' in selection) != ('repositories' in selection), 'Choose one repository selection form'
        repositories = selection.get('repositories', [selection.get('repository')])
        assert isinstance(repositories, list) and repositories and all(isinstance(repo, str) and repo for repo in repositories)
        assert len(set(repositories)) == len(repositories), 'Duplicate repository in batch selection'
        expected = {pid for pid, event in checkpoint_latest.items()
                    if train[pid]['repository'] in repositories
                    and event['category_id'] in selection['discovery_categories']}
        if 'candidate_count' in selection:
            assert len(expected) == selection['candidate_count'], 'Batch candidate count does not match exhaustive selection'
        assert {item['pair_id'] for item in batch['reviews']} == expected
        assert len(batch['reviews']) == len(expected), 'Duplicate case within a review batch'
        for item in batch['reviews']:
            pid = item['pair_id']
            assert pid in train and train[pid]['split'] == 'train'
            assert item['review_revision'] == reviewed.get(pid, {}).get('review_revision', 0)+1
            event = event_for_revision[(pid, item['source_discovery_revision'])]
            assert checkpoint_latest[pid] == event
            assert item['existing_narrow_leaf'] is None, 'Explicitly validate/version a proposed narrow-leaf mapping before using it'
            for field in ('mechanism', 'taxonomy_boundary', 'contract_reason', 'context_reason',
                          'security_reason', 'negative_reason', 'subset_reason', 'dependence_reason'):
                assert isinstance(item[field], str) and item[field]
            assert item['open_questions'] and all(isinstance(q, str) and q for q in item['open_questions'])
            assert item['existing_contract'] in {'supported_under_retained_contract', 'unresolved_runtime_support', 'unresolved_existing_contract', 'feature_expansion_not_prior_repair', 'no_selected_runtime_repair'}
            assert item['selected_relevance'] in {'local_repair_supported', 'conditional_runtime_repair', 'unresolved_supported_case', 'coordinated_component_not_isolated', 'new_feature_implementation'}
            assert item['function_only_context'] in {'conditional_on_ordinary_api_semantics', 'requires_missing_project_contract'}
            assert item['security_screen'] in {'functional_witness_no_demonstrated_security_boundary', 'unresolved_boundary', 'demonstrated_security_boundary'}
            assert item['paired_negative_scope'] in {'mechanism_local_only', 'not_established_for_selected_component'}
            assert item['experimental_subset_proposal'] in {'conditional_retain', 'defer_missing_context', 'defer_security_boundary', 'defer_existing_contract', 'defer_selected_attribution', 'propose_feature_exclusion', 'propose_nonrepair_exclusion', 'defer_task_scope', 'defer_paired_negative'}
            proposal = item['experimental_subset_proposal']
            if item.get('paired_negative_assessment') in UNRESOLVED_PAIRED_NEGATIVE_ASSESSMENTS:
                assert proposal == 'defer_paired_negative', 'Unresolved after-contract failure needs an explicit paired-negative deferral'
            if item['existing_contract'] == 'feature_expansion_not_prior_repair':
                assert proposal == 'propose_feature_exclusion', 'Feature expansion needs an explicit exclusion proposal'
            if item['existing_contract'] == 'no_selected_runtime_repair':
                assert proposal == 'propose_nonrepair_exclusion', 'No selected runtime repair needs an explicit nonrepair exclusion proposal'
            if 'additional_after_concerns' in item:
                assert item['additional_after_concerns'] and all(isinstance(reason, str) and reason for reason in item['additional_after_concerns'])
                assert item['paired_negative_scope'] == 'not_established_for_selected_component'
                assert proposal != 'conditional_retain', 'Additional after-contract concerns cannot be silently retained'
            if item.get('task_scope') == 'unresolved_nonstyle_eligibility':
                assert proposal == 'defer_task_scope', 'Unresolved task scope needs an explicit scope deferral'
            if proposal == 'conditional_retain':
                assert event['review_status'] == 'assistant_supported'
                assert item['existing_contract'] == 'supported_under_retained_contract'
                assert item['selected_relevance'] == 'local_repair_supported'
                assert item['function_only_context'] == 'conditional_on_ordinary_api_semantics'
                assert item['security_screen'] == 'functional_witness_no_demonstrated_security_boundary'
                assert item['paired_negative_scope'] == 'mechanism_local_only'
            elif proposal == 'defer_missing_context':
                assert item['function_only_context'] == 'requires_missing_project_contract'
            elif proposal == 'defer_security_boundary':
                assert item['security_screen'] == 'unresolved_boundary'
            elif proposal == 'defer_existing_contract':
                assert item['existing_contract'] in {'unresolved_runtime_support', 'unresolved_existing_contract'}
            elif proposal == 'defer_selected_attribution':
                assert item['selected_relevance'] == 'coordinated_component_not_isolated'
                assert item['paired_negative_scope'] == 'not_established_for_selected_component'
            elif proposal == 'defer_paired_negative':
                assert item['existing_contract'] == 'supported_under_retained_contract'
                assert item['paired_negative_scope'] == 'not_established_for_selected_component'
                assert item.get('paired_negative_assessment') in UNRESOLVED_PAIRED_NEGATIVE_ASSESSMENTS
                assert isinstance(item.get('paired_negative_assessment_reason'), str) and item['paired_negative_assessment_reason']
            elif proposal == 'propose_feature_exclusion':
                assert item['existing_contract'] == 'feature_expansion_not_prior_repair'
                assert item['selected_relevance'] in {'new_feature_implementation', 'coordinated_component_not_isolated'}
                assert item['paired_negative_scope'] == 'not_established_for_selected_component'
                assert event['review_status'] == 'assistant_proposed_exclusion'
            elif proposal == 'propose_nonrepair_exclusion':
                assert item['existing_contract'] == 'no_selected_runtime_repair'
                assert item['selected_relevance'] == 'coordinated_component_not_isolated'
                assert item['paired_negative_scope'] == 'not_established_for_selected_component'
                assert event['review_status'] == 'assistant_proposed_exclusion'
            elif proposal == 'defer_task_scope':
                assert item['existing_contract'] == 'supported_under_retained_contract'
                assert item['task_scope'] == 'unresolved_nonstyle_eligibility'
                assert isinstance(item['task_scope_reason'], str) and item['task_scope_reason']
            row = train[pid]
            if 'redirect_analysis' in item:
                flow = item['redirect_analysis']
                assert flow['parameter'] == 'next' and flow['parameter_source'] in {'GET', 'POST'}
                assert f"request.{flow['parameter_source']}.get(" in row['before'], 'Redirect parameter mapping must match the selected before source'
                assert flow['operation_gate'] in {'POST_required', 'decorated_consumer_required', 'authenticated_early_return', 'unauthenticated_early_return'}
                assert isinstance(flow['prerequisites'], str) and flow['prerequisites']
                if flow['parameter_source'] == 'POST':
                    assert "method='POST'" in row['after'], 'POST redirect analysis requires matching explicit helper selection'
                if flow['operation_gate'] == 'POST_required':
                    assert any(gate in row['before'] for gate in ('@require_POST', 'is_post(request)', "request.method == 'POST'")), 'POST operation gate needs retained selected-source evidence'
            proofs = {}
            for side in ('before', 'after'):
                key = (pid, side)
                if key not in source_cache:
                    source_cache[key] = audit.source(row, side)
                proofs[side] = source_cache[key][1]
            commit = (next(commit for commit in metadata[row['hapy_case_id']]['commits']
                           if commit['index'] == row['hapy_commit_index'])
                      if row['source'] == 'HaPy-Bug' else None)
            anchors = []
            assert {a['side'] for a in item['anchors'] if a['kind'] == 'archive'} == {'before', 'after'}
            for anchor in item['anchors']:
                kind = anchor['kind']
                if kind == 'archive':
                    side = anchor['side']
                    text = ''.join(source_cache[(pid, side)][0])
                    evidence = dict(kind=kind, side=side, source=proofs[side])
                elif kind == 'fix':
                    assert commit is not None, 'Fix anchors require retained HaPy commit metadata; use verified archive/supplement evidence for other sources'
                    text = commit['diff']
                    evidence = dict(kind=kind, metadata_file='HAPY_BUG_CASE_METADATA.json',
                                    case_id=row['hapy_case_id'], commit_index=row['hapy_commit_index'],
                                    diff_sha256=audit.sha(text))
                elif kind == 'supplement':
                    source_name = anchor['file']
                    assert source_name in SUPPLEMENTAL_PINS
                    if source_name not in supplemental_cache:
                        supplemental_cache[source_name] = audit.load(source_name)['sources']
                    sources = [source for source in supplemental_cache[source_name]
                               if source.get('path') == anchor['path']
                               and ('ref' not in anchor or source.get('ref') == anchor['ref'])]
                    assert len(sources) == 1, 'Supplemental evidence requires an unambiguous path/ref'
                    source = sources[0]
                    assert audit.sha(source['text']) == source['sha256']
                    text = source['text']
                    evidence = dict(kind=kind, file=source_name, **supplemental_origin(source, train, source_cache),
                                    path=source.get('path'), ref=source.get('ref'),
                                    source_kind=source.get('source_kind', 'retained_source_text'),
                                    source_sha256=source['sha256'])
                    if source.get('source_kind', '').startswith('mutable_'):
                        evidence.update(collected=source['collected'], limitation=source['limitation'])
                    if source.get('source_kind') in BODY_SNAPSHOT_KINDS:
                        evidence.update(created_at=source['created_at'], updated_at=source['updated_at'],
                                        html_url=source['html_url'], api_response_sha256=source['api_response_sha256'])
                else:
                    raise ValueError(f'Unknown inert evidence-anchor type: {kind}')
                anchors.append(dict(**evidence, **retained_anchor(text, anchor['needle'])))
            current = event == latest[pid]
            record = dict(item, batch_id=batch['batch_id'], review_date=batch['review_date'],
                          source_batch_file=name, split='train', researcher_status='pending',
                          proposal_status='assistant_proposal_not_approved',
                          source_discovery_category=event['category_id'],
                          source_event_sha256=audit.sha(json.dumps(event, sort_keys=True, separators=(',', ':'), ensure_ascii=False)),
                          matches_latest_discovery_event=current, mechanical_family_id=families[pid],
                          inspected_code_sha256=event['inspected_code_sha256'],
                          selected_source_proofs=proofs, verified_evidence_anchors=anchors,
                          audited_independent_issue_count=None)
            records.append(record)
            reviewed[pid] = record
    active = {pid: record for pid, record in reviewed.items() if record['matches_latest_discovery_event']}
    result = dict(schema_version='1', scope='training_only', status='assistant_proposals_not_approved',
                  researcher_status='pending', records=records,
                  current_reviewed_candidates=len(active), remaining_candidates=len(train)-len(active),
                  stale_review_candidates=sorted(set(reviewed)-set(active)),
                  proposal_counts=dict(sorted(Counter(r['experimental_subset_proposal'] for r in active.values()).items())),
                  interpretation='Reviewed means separate assistant proposals have been recorded; it does not mean eligibility approval, frozen context sufficiency or independent issue adjudication.')
    return result, active


def dependence_inventory(train, families, latest, plan):
    assert all(row['split'] == 'train' for row in train.values()), 'Dependence review is training-only'
    assert set(train) == set(families) == set(latest)
    family_members = defaultdict(list)
    for pid in sorted(train):
        family_members[families[pid]].append(pid)
    family_records = []
    for fid, members in sorted(family_members.items()):
        provenance = [item for pid in members for item in
                      [train[pid]] + train[pid].get('duplicate_pair_provenance', [])]
        family_records.append(dict(
            mechanical_family_id=fid, pair_ids=members,
            repositories=sorted({train[pid]['repository'] for pid in members}),
            fixing_commits=sorted({item['fixing_commit'] for item in provenance}),
            recorded_cve_ids=sorted({cve for item in provenance
                                    for cve in item.get('cves', []) + item.get('commit_linked_cves', [])}),
            discovery_categories=sorted({latest[pid]['category_id'] for pid in members if latest[pid]['category_id']}),
            statuses=status_counts(members, latest),
            alias_backport_fork_and_root_cause_review='pending',
            audited_independent_issue_count=None,
        ))

    edges = []
    def add_edge(kind, left, right, evidence):
        left, right = sorted((left, right))
        edges.append(dict(link_id='training-link:' + audit.sha(kind+'\n'+left+'\n'+right)[:20],
                          relation=kind, pair_ids=[left, right],
                          within_existing_mechanical_family=families[left] == families[right],
                          evidence=evidence, root_cause_equivalence='not_adjudicated'))

    # Exact and AST snapshot matches are evidence links, not automatic root-cause merges.
    for kind, suffix in (('shared_exact_version', '_sha256'), ('shared_ast_version', '_ast_sha256')):
        buckets = defaultdict(list)
        for pid, row in sorted(train.items()):
            for side in ('before', 'after'):
                buckets[(row['repository'], row[side+suffix])].append((pid, side))
        linked = defaultdict(list)
        for (repository, digest), endpoints in sorted(buckets.items()):
            for (left, left_side), (right, right_side) in combinations(endpoints, 2):
                if left == right:
                    continue
                if left > right:
                    left, right, left_side, right_side = right, left, right_side, left_side
                linked[(left, right)].append(dict(repository=repository, digest=digest,
                                                  left_side=left_side, right_side=right_side))
        for (left, right), matches in sorted(linked.items()):
            add_edge(kind, left, right, dict(matches=matches,
                limitation='Identical syntax/version does not prove the same defect or chronological ancestry; short helper coincidences and copy/fork history require review.'))

    histories = defaultdict(list)
    spans = defaultdict(list)
    for pid, row in sorted(train.items()):
        histories[(row['repository'], row['path'], row['qualified_function'])].append(pid)
        spans[(row['repository'], row['fixing_commit'], row['path'])].append(pid)
    for (repository, path, qualified), members in sorted(histories.items()):
        for left, right in combinations(members, 2):
            if train[left]['fixing_commit'] != train[right]['fixing_commit']:
                add_edge('same_function_revision_history', left, right,
                         dict(repository=repository, path=path, qualified_function=qualified,
                              limitation='Repeated function identity is a version-dependence review cue, not proof of a shared root cause or chronology.'))
    for _, members in sorted(spans.items()):
        for left, right in combinations(members, 2):
            intersections = {}
            for side in ('before', 'after'):
                lo = max(train[left][side+'_start_line'], train[right][side+'_start_line'])
                hi = min(train[left][side+'_end_line'], train[right][side+'_end_line'])
                left_path = train[left].get(side+'_path', train[left]['path'])
                right_path = train[right].get(side+'_path', train[right]['path'])
                if left_path == right_path and lo <= hi:
                    intersections[side] = dict(path=left_path, intersection=[lo, hi],
                        left_span=[train[left][side+'_start_line'], train[left][side+'_end_line']],
                        right_span=[train[right][side+'_start_line'], train[right][side+'_end_line']])
            if intersections:
                add_edge('same_fix_source_span_overlap', left, right, dict(sides=intersections,
                    limitation='Nested/overlapping selected text must not create independent observations; compare paired spans and task eligibility.'))

    for review in plan['curated_lineage_reviews']:
        earlier, later = review['earlier_pair_id'], review['later_pair_id']
        assert earlier in train and later in train
        assert train[earlier]['after_sha256'] == train[later]['before_sha256']
        assert train[earlier]['repository'] == train[later]['repository']
        add_edge(review['relation'], earlier, later,
                 dict(earlier_pair_id=earlier, later_pair_id=later,
                      shared_exact_sha256=train[earlier]['after_sha256'],
                      ledger_revisions={pid: latest[pid]['revision'] for pid in (earlier, later)},
                      evidence=review['evidence'], proposal=review['proposal'],
                      researcher_status='pending'))

    edges.sort(key=lambda edge: edge['link_id'])
    assert len({edge['link_id'] for edge in edges}) == len(edges)
    # Components organize review of possible dependence. They deliberately retain
    # distinct mechanical families and never become independent issue identities.
    parent = {fid: fid for fid in family_members}
    def root(fid):
        while parent[fid] != fid:
            parent[fid] = parent[parent[fid]]
            fid = parent[fid]
        return fid
    for edge in edges:
        left, right = (families[pid] for pid in edge['pair_ids'])
        parent[root(left)] = root(right)
    blocks = defaultdict(list)
    for fid in sorted(family_members):
        blocks[root(fid)].append(fid)
    records, block_for_pair = [], {}
    for fids in sorted(blocks.values(), key=lambda values: tuple(values)):
        bid = 'dependence-review:' + audit.sha('\n'.join(fids))[:20]
        members = sorted(pid for fid in fids for pid in family_members[fid])
        for pid in members:
            block_for_pair[pid] = bid
        records.append(dict(review_block_id=bid, mechanical_family_ids=fids, pair_ids=members,
                            proposed_issue_merge='not_decided', audited_independent_issue_count=None))
    assert set(block_for_pair) == set(train)
    assert sum(len(record['mechanical_family_ids']) for record in records) == len(family_members)
    return dict(scope='training_only', status='mechanical_and_evidence_linked_review_inventory_not_independent_issue_counts',
                family_count=len(family_records), families=family_records,
                edge_counts=dict(sorted(Counter(edge['relation'] for edge in edges).items())), edges=edges,
                review_blocks=records,
                limitations=['Repository dependence remains even between separate review blocks.',
                             'CVE aliases/backports/forks and semantic clones need evidence beyond these exact/AST/name/span links.',
                             'Connected blocks organize conservative dependence review; neither blocks nor families are audited independent issue counts.']), block_for_pair


def artifacts():
    train, families, events, latest = training_inputs()
    supplemental = verify_supplemental_evidence()
    plan = audit.load(PLAN)
    definitions = audit.load('CATEGORY_AUDIT_CATEGORIES.json')
    assert plan['source_taxonomy_version'] == definitions['version'] == '0.42'
    assert plan['status'] == 'assistant_proposal_training_only_not_frozen'
    assert plan['researcher_status'] == 'pending'
    cats = {category['category_id']: category for category in definitions['categories']}
    primary = {}
    for parent in plan['parents']:
        for cid in parent['leaf_categories']:
            assert cid in cats and cid not in primary, cid
            assert cats[cid]['domain'] == parent['domain'], cid
            primary[cid] = parent['parent_id']
    assert set(primary) == set(cats) and len(primary) == 113
    assert len({parent['parent_id'] for parent in plan['parents']}) == len(plan['parents'])
    assert all(train[c['training_seed']]['split'] == 'train' for c in cats.values())
    for boundary in plan['priority_boundary_reviews']:
        assert set(boundary['leaf_categories']) <= set(cats)

    dependence, block_for_pair = dependence_inventory(train, families, latest, plan)
    reviews, reviewed = case_reviews(train, families, events, latest)
    links_for_pair = defaultdict(list)
    for edge in dependence['edges']:
        for pid in edge['pair_ids']:
            links_for_pair[pid].append(edge['link_id'])
    counts, crosswalk = [], []
    unsupported_leaves = []
    for cid, definition in sorted(cats.items()):
        ids = sorted(pid for pid, event in latest.items() if event['category_id'] == cid)
        supported = [pid for pid in ids if latest[pid]['review_status'] == 'assistant_supported']
        if not supported:
            unsupported_leaves.append(cid)
        crosswalk.append(dict(discovery_category=definition,
            proposed_parent_id=primary[cid], mapping_status='assistant_proposed_not_approved',
            training_pair_ids=ids, statuses=status_counts(ids, latest),
            supported_mechanical_family_count=len({families[pid] for pid in supported}),
            seed_review_status=latest[definition['training_seed']]['review_status'],
            supported_training_evidence='present_provisionally' if supported else 'none_at_checkpoint',
            eligible_pairs=None, audited_independent_issue_count=None))

    stream = io.StringIO(newline='')
    writer = csv.DictWriter(stream, fieldnames=['proposed_parent_id', 'split', 'discovery_leaves', 'reviewed_pairs',
        *STATUSES, 'supported_mechanical_family_union', 'supported_repository_union',
        'researcher_approved_pairs', 'eligible_pairs', 'audited_independent_issue_count'])
    writer.writeheader()
    for parent in plan['parents'] + [dict(parent_id='UNRESOLVED', leaf_categories=[])]:
        parent_id = parent['parent_id']
        members = sorted(pid for pid, event in latest.items()
                         if primary.get(event['category_id'], 'UNRESOLVED') == parent_id)
        supported = [pid for pid in members if latest[pid]['review_status'] == 'assistant_supported']
        record = dict(proposed_parent_id=parent_id, split='train', discovery_leaves=len(parent['leaf_categories']),
            reviewed_pairs=len(members), **status_counts(members, latest),
            supported_mechanical_family_union=len({families[pid] for pid in supported}),
            supported_repository_union=len({train[pid]['repository'] for pid in supported}),
            researcher_approved_pairs=0, eligible_pairs='', audited_independent_issue_count='')
        writer.writerow(record)
        counts.append(record)
    assert sum(record['reviewed_pairs'] for record in counts) == 742
    assert all(sum(record[status] for record in counts) == sum(e['review_status'] == status for e in latest.values()) for status in STATUSES)

    work = []
    for pid in sorted(train, key=lambda pid: (STATUSES.index(latest[pid]['review_status']) if latest[pid]['review_status'] != 'assistant_supported' else 3, pid)):
        row, event = train[pid], latest[pid]
        review = reviewed.get(pid)
        required = ['Confirm existing functional/security contract and selected-function attribution.',
                    'Decide function-only eligibility using a common before-only bounded input protocol.',
                    'Confirm mechanism-local paired-negative scope and residual after behavior.',
                    'Reconcile issue identity, source overlap, version lineage and repository dependence.']
        required.append('Establish lower-trust provenance, actual security boundary and reachable consumer.'
                        if row['issue_group'] == 'security_candidate' else
                        'Perform explicit non-security screening; generic-bug provenance does not establish it.')
        work.append(dict(pair_id=pid, split='train', repository=row['repository'], path=row['path'],
            qualified_function=row['qualified_function'], fixing_commit=row['fixing_commit'],
            source_issue_group=row['issue_group'], latest_revision=event['revision'],
            latest_event_sha256=audit.sha(json.dumps(event, sort_keys=True, separators=(',', ':'), ensure_ascii=False)),
            current_review_status=event['review_status'], researcher_status='pending',
            discovery_category_id=event['category_id'], proposed_parent_id=primary.get(event['category_id']),
            mechanical_family_id=families[pid], dependence_review_block_id=block_for_pair[pid],
            dependence_link_ids=links_for_pair[pid],
            review_track={'assistant_ambiguous': 'resolve_ambiguity',
                          'assistant_proposed_exclusion': 'confirm_or_reverse_proposed_exclusion',
                          'assistant_supported': 'reassess_supported_under_same_rules'}[event['review_status']],
            eligibility_decision='pending', function_only_context_decision='pending',
            paired_negative_decision='pending', independent_issue_decision='pending',
            consolidation_review_state='assistant_proposals_recorded' if review else 'not_started_or_stale',
            consolidation_review_reference=dict(file=OUTPUTS['reviews'], batch_id=review['batch_id'],
                review_revision=review['review_revision'], experimental_subset_proposal=review['experimental_subset_proposal']) if review else None,
            required_review=required, retrieval_cues=cue_matches(event),
            current_reason=event['reason'], current_function_only_observability=event['function_only_observability'],
            current_negative_scope=event['negative_scope'], current_open_questions=event['open_questions'],
            evidence_references=event['evidence']))
    assert {record['pair_id'] for record in work} == set(train) and len(work) == 742
    assert all(record['researcher_status'] == 'pending' for record in work)

    parent_names = {p['parent_id']: p['name'] for p in plan['parents']}
    cues = Counter(route for record in work for route in record['retrieval_cues'])
    totals = Counter(event['review_status'] for event in latest.values())
    report = [
        '# Training-only category consolidation: first proposal', '',
        f"Proposal v{plan['version']} — {plan['created']}. **Researcher approval is not ready.**", '',
        '## Checkpoint and scope', '',
        f"- All **{len(train)} training candidates / {len(events)} ledger events** are represented: **{totals['assistant_supported']} supported, {totals['assistant_ambiguous']} ambiguous, {totals['assistant_proposed_exclusion']} proposed exclusions**.",
        f"- **113 discovery leaves → {len(plan['parents'])} proposed reporting parents**. Every original leaf definition/seed and latest decision is retained. This is a hierarchy proposal, not a frozen replacement taxonomy or {len(plan['parents'])} established evaluation classes.",
        '- Held-out references and predictions do not contribute to these definitions, counts, review cues or dependence links. Protected split/canonical bytes are checked for integrity only.',
        '- All eligibility, context sufficiency, paired-negative and independently adjudicated issue decisions remain pending. Empty independent/eligible count fields mean unknown.',
        '- Families, parent counts and connected dependence blocks are mechanical review units, not independent observations. Category rows must not be summed for global family counts.', '',
        '## Proposed parent crosswalk', '',
        '| Parent | Leaves | Supported | Ambiguous | Proposed exclusion | Supported family union |',
        '|---|---:|---:|---:|---:|---:|',
    ]
    for record in counts:
        name = parent_names.get(record['proposed_parent_id'], 'No discovery category assigned')
        report.append(f"| {record['proposed_parent_id']}: {name} | {record['discovery_leaves']} | {record['assistant_supported']} | {record['assistant_ambiguous']} | {record['assistant_proposed_exclusion']} | {record['supported_mechanical_family_union']} |")
    report += ['', '### Boundaries that require explicit decisions', '']
    report += [f"- **{', '.join(item['leaf_categories'])}**: {item['decision']}" for item in plan['priority_boundary_reviews']]
    report += ['', 'No current supported training cases for: ' + ', '.join(f'`{cid}`' for cid in unsupported_leaves) + '.',
               'Parent support must not be used to promote these leaves or their ambiguous candidates.', '',
               '## Exhaustive candidate work queue', '',
               '- `CATEGORY_AUDIT_CONSOLIDATION_REVIEW_QUEUE.jsonl` preserves 742 original IDs with current reasons, evidence references, questions, mechanism-local negative scope and exact latest-event digest.',
               f"- It routes {totals['assistant_ambiguous']} cases to ambiguity resolution, {totals['assistant_proposed_exclusion']} to confirm/reverse exclusion and all {totals['assistant_supported']} supported cases to the same contract/context/security/negative/independence checks.",
               '- Literal-text cues only help retrieve relevant existing notes; they are not new findings or automatic eligibility judgments. A phrase may occur in a negation or caution. Exact field/excerpt is retained.', '',
               '| Retrieval route (overlapping, not adjudicated counts) | Candidates with cue |', '|---|---:|']
    report += [f'| {route} | {cues[route]} |' for route in CUES]
    report += ['', '## Dependence review inventory', '',
               f"- **{dependence['family_count']}** existing mechanical training families; **{len(dependence['review_blocks'])}** connected dependence-review blocks after the explicit links below.",
               '- Family records preserve all candidates, statuses, repositories, commits and recorded CVE IDs; aliases/backports/forks/root causes remain pending.',
               '- Shared exact/AST versions, same-function histories and same-fix source overlaps are recorded separately. Matches do not establish chronological ancestry or the same defect.',
               '- Connected blocks may contain distinct issues and remain dependent through repositories even when disconnected. They are not proposed automatic canonical merges.', '',
               '| Evidence-link type | Pair links |', '|---|---:|']
    report += [f'| {kind} | {count} |' for kind, count in dependence['edge_counts'].items()]
    report += ['', '### Evidence-backed priority lineages', '']
    for item in plan['curated_lineage_reviews']:
        report += [f"- `{item['earlier_pair_id']}` → `{item['later_pair_id']}`: {item['evidence']} {item['proposal']}"]
    report += ['', '## Evidence-based consolidation reviews', '',
               f"- **{reviews['current_reviewed_candidates']} / {len(train)}** candidates have separate current assistant proposals; **{reviews['remaining_candidates']}** remain. This is proposal coverage, not approved eligibility.",
               '- `CATEGORY_AUDIT_CONSOLIDATION_CASE_REVIEWS.json` verifies each proposal against its fixed ledger checkpoint, archived before/after source and exact retained evidence anchors.',
               '- First batch: all eight Scrapy broad correctness cases. One discovery revision changes command-discovery eligibility from supported to ambiguous after pre-fix documentation establishes only a Python2/2.7 advertised installation contract; a prior Python3 commitment remains unresolved.',
               '- Second batch: all nine Thefuck broad correctness cases. A pinned direct-CLI/inherited-consumer path resolves the Zsh absent-environment witness, prompting a discovery revision from ambiguous to supported while function-only admission is deferred. Pre-fix setup establishes existing Python2 support for the shelf repair; PHP dispatch tests for output is None, not an empty string. Git support-expansion contracts, producer-component attribution, shell semantics and cache trust remain explicit questions.',
               '- Third batch: all five Ansible broad correctness cases. Attributed EOS issue evidence distinguishes global versus VRF-scoped enablement and supports the former tentative mechanism; device-context admission stays deferred. Collection support is narrowed to top-level unknown-version equality syntax rather than the separately changed dependency warning policy. Exact pre-fix dict_diff confirms overlapping VLAN update/removal keys. Conditional API/CLI knowledge and precise context boundaries remain unfrozen.',
               '- Fourth batch: all three Cookiecutter broad correctness cases. Pinned pre-fix docs and attributed issue/PR history support two multi-hook feature-exclusion proposals for the matching scalar-to-list finder/runner migration. Failed-pre-hook cleanup is revised from supported to ambiguous because an existing cleanup guarantee is unestablished: the old generator already stops, and the selected after snapshot still returns None. Later docs/review requests do not retroactively supply that contract or replace the retained intermediate snapshot. Existing-directory deletion and swallowed cleanup failures remain explicit residuals.',
               '- Fifth batch: all twenty Black broad correctness cases. Exact grammar/CST consumers distinguish real parsing, bracket-state, stability and invalid-output mechanisms from layout-only evidence. Three parser/driver configuration-plumbing discovery findings become ambiguous for selected attribution; the shared modern-tokenizer failure stays supported. Explicit fmt:on control has an old contract but unresolved non-style task scope, kept separate from a missing contract. Successive tokenizer and comma-builder hashes link distinct follow-up mechanisms without proving independent issues. All source/fixtures remain inert.',
                '- Sixth batch: all 31 Keras broad correctness cases. Fourteen contextually supported repairs remain missing-context deferrals; multi-character text separation has one conditional-retain proposal. Thirteen prior runtime/API or feature-contract questions remain explicit. Three foreign-Sequence recognition discoveries become ambiguous because exact old adapters do not prove inherited flow returns them or promises automatic step inference; the nested reconstruction signal producer also becomes ambiguous for selected attribution. Two coordinated components are deferred. Image preprocessing has a supported old ordering duty but an unresolved after-side PIL-versus-NumPy callback regression, recorded as a separate paired-negative deferral. No backend, model, callback, initializer, image, generator or dataset test is run.',
                 '- Seventh batch: all 58 pandas broad correctness cases. One locally documented tuple/list mismatch is conditionally retained; 42 proposals defer missing project context, eight defer prior contract/runtime, five defer selected attribution and two propose feature exclusion. Exact old groupby docs establish the unobserved categorical-product promise; exact old BaseIndexer whitelist explicitly excludes count. Two count discoveries become proposed exclusions and three correct-old-interface caller discoveries become ambiguous. Native source strengthens engine and nullable-conversion investigation without certifying lifetime or non-nanosecond nonmutation. Old API conflicts, fast-path-only evidence and narrow residuals remain explicit. No pandas, NumPy, native, parser, dataframe or dataset test is run.',
                  '- Eighth batch: all 34 pandas dtype-preservation/semantic-type-validation candidates. Twenty-two defer critical project context, five defer prior contracts, four defer selected attribution and three defer paired negatives. Homogeneous extension transpose can collapse duplicate labels through dictionary construction. Matched temporal lookup repairs return source-sized -1 arrays despite old target-index/missing-position contracts; part of that pattern already existed, so after failure is recorded without invented introduction chronology. Three temporal rejection discoveries become ambiguous for old-policy uncertainty and one no-match replacement discovery becomes ambiguous for an incomplete selected-path trace. Concrete aggregate/asof value or label loss remains distinct from changed dtype/rejection policy and correct-old-interface callers. All source and tests remain inert.',
                   '- Ninth batch: all 50 pandas alignment/recovery/options/metadata/error/shape/lookup/encoding candidates. Thirty-one defer critical context, nine defer prior contracts, eight defer selected attribution and two defer paired negatives. Seven discovery findings become ambiguous after old acceptance tests/docs or matched caller admission undermine a prior-defect claim. Exact old right-merge and union docs establish ordering duties despite API-change framing. Categorical datetime method repair still loses custom source labels; normalized margins reject tuple column-margin keys. These after failures retain supported old duties without invented introduction chronology. Old helper compatibility, native dimensionality and successive range/unstack/scalar-lookup histories remain explicit; no dataset or dependency programs are run.',
                    '- Tenth batch: all remaining 32 pandas training candidates, including 19 unclassified cases. Eleven defer critical context, two defer prior contracts, sixteen defer selected attribution, one defers a paired negative and two propose feature exclusion. Exact old multidimensional-index acceptance with a deprecation warning changes one discovery finding to ambiguous; newly versioned pickle URL admission changes two to proposed exclusions. The missing-text capacity repair casts ordinary nonmissing integers to Unicode width determined only by na_rep, introducing truncation; its paired negative is explicitly deferred. Correct old property/standard-deviation/frequency/NA/merge/copy interfaces and retired scalar extraction remain separate from their coordinated public repairs. All 174 pandas candidates now have current proposals; all source traces remain inert and provisional.',
                    '- Eleventh batch: all remaining 42 Keras training candidates. Fourteen defer critical context, four defer old contracts, nine defer selected attribution and fifteen propose feature exclusion. Explicit output_size/state-order changes, transpose dilation, optional best-weight restoration and optional Sequence steps are new API/policy. Old worker-failure tests explicitly expect StopIteration; three error-propagation discoveries become ambiguous. The downloader cache override becomes ambiguous because old backend configuration support does not alone establish a download-cache environment promise. Fifteen ambiguous discoveries become proposed feature exclusions. Temporal metric axes, singleton CTC/regression axes, heterogeneous state masks/shapes, inclusive time-series endpoints, Windows CSV records, unknown-target progress and all-masked finite loss retain contextual support. All 73 Keras candidates now have current proposals; the prior image-callback after failure stays unresolved. No dataset/dependency program executes.',
                '- Twelfth batch: all remaining 40 Scrapy training candidates. Ten defer missing context, thirteen defer prior contracts, sixteen defer selected attribution and one defers a paired negative. Nine supported discoveries become ambiguous after exact old runtime promises or acceptance policies undermine a prior-defect assertion. Thirteen logging edits coordinate migration away from a parent-logger filter; a project traceback-routing failure does not isolate thirteen local algorithm defects. Gzip recovery still has a source-deduced zero-size suffix replay boundary under retained CPython2.7.12 semantics, recorded as a residual failure without invented introduction chronology. All 48 Scrapy candidates now have current proposals; no dependency or dataset code executes.',
                '- Thirteenth batch corrects only the security-screen metadata for the Scrapy credential-destination-scope review, preserving authored batch012. Its already explicit crawler-owned credential disclosure trace is now marked demonstrated_security_boundary; the missing-context proposal, bounded negative and discovery event are unchanged. This adds no newly reviewed candidate or approval.',
                '- Fourteenth batch: all remaining 30 Black training candidates, including the CVEfixes leading-tab regex case. Four defer missing context, four defer prior contracts, seventeen defer selected attribution, two defer non-style scope, one proposes feature exclusion and two propose nonrepair exclusion. Two supported discoveries become ambiguous: restricted-environment process-pool fallback and missing-config exit classification lack established old support/policy promises. A new helper introduces empty-input failures in the file/stdin after routes, recorded separately from unresolved old newline-preservation duty. Annotation-only scheduler documentation and AST error guidance are nonrepair exclusions, not forced into feature-expansion labels. The regex availability boundary needs its omitted pattern and untrusted-source path. All 50 Black candidates now have current proposals; formatter, parser, regex, CLI, process pools and upstream tests remain inert.',
                '- Fifteenth batch: all 29 Spirit training candidates in one shared CVE/fix family, including overlapping guest_only factory/wrapper spans. Four wired auth-entry branches have direct GET-link navigation witnesses but defer missing before-only context. Twenty-five defer security-boundary adjudication: twenty-three POST-gated outcomes need realistic victim/CSRF/role/form delivery and two decorator-utility spans need an installed consumer. Nineteen parameter sources are POST; ten are GET, of which four still require a POST operation. Invalid forms, duplicate submissions, non-AJAX paths and fixed/anonymous branches remain distinct. Matching helper rejects ordinary external HTTPS next to root, not the configured fallback; allowed_hosts=None supplies an empty host set. Legacy and modern Django matchers are pinned inside the old >=2.2,<3.2 range. All discovery source-to-sink findings and ledger bytes are preserved; no request, view, ORM, browser, framework or upstream test executes.',
                '- Sixteenth batch: all 21 remaining Thefuck training candidates, completing all 30. Nine defer missing context, three old contracts, two selected attribution and two paired negatives; three propose feature/policy exclusions and two nonrepair exclusions. One supported discovery becomes ambiguous: Settings.update obeys its documented/direct-tested overwrite API while its defaults-only wrapper has a conflicting promise. Matched equality migration leaves old first-two uniqueness equivalent and introduces cached-first duplicate reappearance in the companion filter. Explicit upstream composition introduces quoting loss; the later terminal-option repair retains quoting/cached-token concerns. Old force-push/alias policies, targeted Vagrant output and line-only editor duties are preserved. Exact old Windows CI supports PATH-separator duty; Fish version startup-loop delivery remains unresolved and fish -c is not -i. All shell, parser, Git, archive, CLI, dependency and upstream-test programs remain inert.',
                 '- Seventeenth batch clarifies Git grammar in the complete three-case Thefuck command-rewrite leaf, superseding one metadata overstatement and revalidating two proposals unchanged. Historical Git source shows -u is a Boolean flag: the old trailing repeated flag can be accepted, so the newly added second pop introduces a terminal-option regression on a previously usable suggestion. Keep this separate from duplicated positional repository operands and new quoting loss. Preserve batch016, all discovery events, proposal counts and dependence; three review revisions are not three new candidates or observations. Comparison Git v2.9.3 does not prove a deployed version, and is never executed.',
                  '- Eighteenth batch: all 21 Synapse training candidates across five mechanical fix families. Ten defer missing context, seven defer security delivery, one defers selected attribution and one defers a paired negative; two propose nonrepair exclusion. Room parsing uses one authoritative body room ID after, rather than rejecting every URI/body mismatch. Outbound-client policy depends on explicitly configured new IP ranges, direct/literal versus proxy resolution and real consumers. The well-known resolver gains a bounded reader; two already-bounded downloader siblings instead migrate helpers and introduce missing-raise/unassigned-length failures. Push wildcard-run compression also loses old explicit character-class matching, so after is not certified clean. Remote media write/read/cleanup paths retain random filesystem suffix constraints; generated local/cache IDs and DB/admin/encoder gates do not inherit the remote advisory. Newly invoking the stricter server validator is coordinated attribution, not an old call-site repair inside that helper. All discovery events remain unchanged, and all application, parser, network, storage and upstream-test programs remain inert.',
                   '- Nineteenth batch: all 20 remaining Ansible candidates, completing all 25. Nine defer missing context, two prior contracts and eight paired negatives; one proposes nonrepair exclusion. Six guest-to-host symlink transfers share one security family, but new dd transfer code introduces one-buffer fetch truncation and unquoted space-containing path failures. PAM tail repair retains singleton deletion failure; banner whitespace repair introduces a coherent newline/idempotence mismatch in its parser, without assigning that sibling failure to every component. Historical Python2 UTF-8 lookup-to-Jinja context changes one discovery to supported; collection malformed-version tolerance becomes ambiguous because old metadata explicitly promises string semver. A third revision narrows supported CLI delimiter duty to documented existing local archives rather than assuming old positional URL support. Pagination, POWER CPU counts, UNC root preservation and omitted subscription quantity retain contextual support. Placeholder wording is nonrepair and sorted diagnostic order lacks an established old promise. All earlier ledger bytes/batches and protected inputs are preserved; source/dependency/platform programs and upstream tests remain inert.',
                   '- Twentieth batch: all 18 Waitress training candidates, including eight null-category components, across four mechanical families. Seven defer security delivery, three missing context, three paired negatives and two selected attribution; three propose nonrepair exclusion. RFC-permitted LF is not unconditionally a bug: differential frontend forwarding/reuse determines header/TE impact. Chunk hardening does not inherit header exploitability; early after rejects valid split CRLF while a different-after sibling buffers it. Old configured header-limit duty is established, but the repair double-counts fragmented prefixes. New ASCII header grammar retains Python3 OBS_TEXT-to-Unicode TE stripping, and chunk dollar anchors retain a terminal-LF route; both are residual failures. The analogous header-LF hypothesis is blocked by its upstream line validator. Socket task ownership, select exception escape and default-preserving plumbing are distinct. Equivalent quote-regex relocation, close announcement and main-loop-only forwarding are nonrepair proposals. All discovery events remain unchanged; source, parsers, sockets, threads and upstream tests stay inert.',
                    '- Twenty-first batch revalidates the complete three-case Waitress socket leaf without adding candidates or discovery events. Deferred100-Continue can run send_continue on the service worker, then use the unchanged defaultTrue flush/send chain and synchronously close a disconnected socket. This is an old residual worker-close route, not a newly introduced optional-flag regression; it explicitly changes the send after-negative proposal to a paired-negative deferral. The two correctlyFalse-controlled selected entries retain their narrow missing-context proposals and do not inherit sibling call-site blame. Preserve batch020 and all source/dependence; the three metadata revisions are not independent observations.',
                    '- Twenty-second batch: all 17 Radicale training candidates across two mechanical families. Five defer missing context, eleven selected attribution and one paired negative. Matched callers establish classification/name effects for five direct Windows path converters; eleven other edits consume an inherited absolute filepath and do not isolate eleven local conversion defects. Fourteen appended discovery revisions promote the five direct caller traces and withdraw nine consumer-attribution claims. The multifilesystem after leaf predicate checks its .props sidecar relative to CWD instead of FOLDER, introducing ordinary valid-leaf misclassification. A pre-existing dict-key-as-Item serialization failure obstructs nonempty multifilesystem calendar disclosure and item deletion. Collection DELETE also eagerly evaluates item.etag even for default If-Match *, narrowing supported deletion to empty/unrecognized-component directories under the remaining gates. Literal-login regex interpolation has an authenticated, provisioned-metacharacter-account boundary under owner policy, not anonymous/default-none exposure. All application, authentication, parser, DAV, Windows/filesystem/storage, dependency programs and upstream tests remain inert.',
                    '- Twenty-third batch: all 16 OpenStack Glance training candidates across three mechanical families. Seven defer missing context, eight security delivery and one paired negative. Exact old SQL visibility versus owner-mutation checks establish both API delete-order defects. The v2 after still passes builtin id to delayed-delete queue naming and scrubber registry lookup, a residual supported failure rather than an introduced ordering regression. Swift add/get errors have exact client-visible HTTP409/404 consumers under single-tenant service credentials and actual backend failure; duplicate registry IDs or zero-size/unreadable images are not that witness. Delete wrappers absorb selected NotFound and log raw URI even after, so do not borrow GET response delivery or certify end-to-end redaction. Two ACL-only locations normally omit passwords/use separate tokens, and three parser-log rows need malformed private input plus unauthorized log readership. All14 Swift/backport rows stay one family; the v2 advisory describes an incomplete v1 fix without settling issue independence. All825 discovery events remain unchanged. Source, authentication, HTTP/parser, DB/SQL, Swift/backend/storage, dependency/application programs and upstream tests stay inert.',
                    '- Twenty-fourth batch: all 11 Vyper training candidates/three mechanical families, including all six null categories. Three defer missing context, five propose nonrepair exclusion, one defers selected attribution, one security delivery and one paired negative. Matched old word-copy capacity, logical bytes equality and strict ABI return duties distinguish local repairs from encoding/hash/calldata refactors. The wrapper adapts to a repaired callee; tuple conversion has no established old security delivery. After returndata decoding uses inferred larger JSON bounds while raw allocation still uses legacy bound1; a no-argument Bytes[96] route reserves128 bytes but allows160 output bytes and overlaps the following native buffer before length-store/copy. Preserve an explicit after-contract failure, without claiming an established introduced regression, executed compiler result or deployed victim. All825 discovery events remain unchanged. Compiler, ABI/AST/IR/type/memory/crypto/EVM/contract, parser, dependency/application programs and upstream tests stay inert.',
                    '- Twenty-fifth batch: all nine Nautobot training candidates/two mechanical families; no null categories exist in this repository. Three defer missing context, four selected attribution and two paired negatives. Standard ErrorDict already escapes filter errors, and RegexValidator truthy params coerce safe messages to ordinary strings before standard ErrorList rendering. The renderer downgrade is needed by new conditional-escaping consumers, but old link/button sinks ignore its marker and old computed fields explicitly escape values; no independent old helper bypass is isolated. Concrete DeviceType import/form/model/message-serialization contracts support a distinct file-author versus importing-operator boundary, not automatic cross-user flash delivery. Append two discovery revisions: renderer supported to ambiguous, import ambiguous to supported; preserve all825 prefix events. After custom links escape their own target fragment so its value is not reserved _blank; after protected-error composition drops an explicitly supported no-URL fallback. Both receive explicit introduced-regression paired-negative deferrals. Repository operations require an active user with coarse change permission and a worker, but old lookup omits per-repository constraints. Nine rows/eight shared HTML representations are not independent issues. All application/dependency, HTML/browser/template/regex/auth/ORM/DB/Git/Celery programs and upstream tests remain inert.',
                     '- Twenty-sixth batch: all eight openapi-python-client training candidates/two mechanical families, including six null categories. One defers missing context, one selected attribution and one paired negative; five propose nonrepair exclusion. Exact title admission and create/write/update-delete consumers support conditional path escape, while the after negative covers only default title-derived lexical paths. Enum key/value data reaches an unchanged Python template and source writer; code execution needs later generated-client import/use. After duplicate checking precedes sanitized-key insertion: ordered A and A-plus-combining-acute values had distinct valid old identifiers but now collapse, losing the legitimate A wire value. Preserve an explicit introduced-regression paired-negative deferral plus residual spaces/hyphens, empty-string indexing and incomplete backslash/newline/quote encoding. Initializer delegation is coordinated, datetime imports match their own version types/templates, Optional opt-outs preserve old annotation behavior and serve a newly changed union runtime consumer, and acronym-range correction is not source sanitization. Preserve all827 discovery events, null categories and prior batches. Eight rows/two families are not independent issues; all generator/dependency/generated/schema/template/regex/filesystem/compiler/import/formatter programs and upstream tests stay inert.',
                     '- Twenty-seventh batch: all eight tlslite-ng training candidates/one mechanical family, including seven null categories. Four defer paired negatives, three old contracts and one proposes nonrepair exclusion. Old TLS premaster processing already randomizes failed/invalid-version results; secret-dependent internal work is not automatically a plaintext network alert or reproduced timing oracle. After PSS adapters lose the k-1 encoded width for modBits=8b+1, native PKCS1 verification loses an explicit fixed signature-width guard under the retained compatible backend comparison, and generated OpenSSL private keys lack d required by the new rejection PRF. Four rows share these three integration mechanisms; they are not independent issue counts. Append four ambiguous discovery revisions withdrawing blanket exclusions for public/private PEM backend promises, PSS public representative-range admission and signing/encryption oversized-input duties. Preserve all827 prefix events, seven null categories and prior authored batches. Native versions are semantic comparisons, not deployed-version proof; all TLS/network/crypto/RSA/PSS/padding/PRF/hash/key/parser/backend/dependency/application programs and upstream tests remain inert.',
                      '- Twenty-eighth batch: all seven OpenStack Nova training candidates/five mechanical families. Three defer missing context and four paired negatives. The first injection patch blocks ordinary dot-dot paths but retains root-only-searchable symlink escape because its realpath check runs unprivileged before root writes. The later root readlink helper closes that permission gap under retained tool/rootwrap contracts; helper-after/later-selected-before equality is not equality of the two selected functions or an approved family merge. DifferentHostFilter removes hint-count-proportional individual API calls, not all host/request/instance work or a constant SQL bound. S3 basename confinement applies to manifest local destinations, not its sibling tarball fix. Protocol producers normalize new rules, but legacy mixed-case rows lose EC2 exact-match revocation and OpenStack exact-repeat duplicate rejection. The firewall additionally calls lower on admitted protocol=None group-wide rules, introducing a generation failure; ICMPv6 type/code omission is residual in both versions. Four after deferrals distinguish three introduced legacy/null-state regressions from residual first-patch confinement failure. Preserve all831 discovery events/statuses/categories, source/dependence and earlier batches. All application, mount/filesystem/rootwrap/command, scheduler/DB, firewall/network/S3/XML/archive/crypto/dependency programs and upstream tests stay inert.',
                      '- Twenty-ninth batch: all seven Zulip training candidates/four mechanical families. Four defer missing context and three security delivery. Invitation validation adopts an invite realm but fresh preregistration follows the request subdomain; final signup still rechecks target email-domain policy, so invitation admission/role transfer is not universal domain bypass. Both after entries bind request/invite realms while preserving invalid-key fallback for open realms; authenticated helper realm preference and existing preregistration states remain qualified. Delegated own-bot management is not authority to grant organization roles, and realm-scoped stream existence is not authorization for private autosubscribe. Three S3 rows share a filename-versus-stored-type header mismatch, but exact before nginx already adds CSP. Script/session consequences require actual nonenforcing browser/configuration delivery; local disk and development redirects are distinct. After uses stored disposition, a signed forced-attachment override and a matching cache discriminator together. No supported after-contract failure is established; negatives remain mechanism-local. Preserve all831 discovery events/statuses/categories, four mechanical families and earlier authored batches. All application/dependency, auth/registration/role/stream/DB, upload/S3/browser/nginx/cache/signing/parser programs, payloads, requests and upstream tests remain inert.',
                      '- Thirtieth batch: all seven Shuup training candidates/one mechanical family. One defers missing context, two old contracts and four security delivery. Pinned django-jinja2.5.0 defaults autoescape=True and ordinary Problem templates interpolate normally; exception reflection is not automatically HTML execution. Xtheme POST and editor preserve CSRF/admin/layout prerequisites, while basket is explicitly CSRF-exempt but its JSON error consumer uses text insertion. Exhausted checkout raises Http404, whose normal Shuup handler discards the exception message; the separate referrer script is unrelated. Admin reasons are fixed/configured permission strings, and its JSON-shaped forbidden branch is unchanged. Generic extraction has a fixed-message product consumer plus an unproven signal-extension producer. Extra-view dispatch instead puts a broad URL-derived missing view directly into an ordinary text/html404 response, bypassing templates; after escapes that value. That supported mechanism still needs external route/theme/runtime context. Preserve six ambiguous/one supported discovery statuses and all831 ledger events. Encoding/display concerns do not establish an independent non-style after-contract failure. Seven functions/one family are not independent issues; all retained programs, requests, payloads and upstream tests remain inert.',
                       '- Thirty-first batch: all seven yt-dlp training candidates/three mechanical families. Six defer missing context and one selected attribution. Nested/outer q-format rows share the same Windows percent-expansion repair, which needs shell=True translation and matching Popen cmd/environment setup. Earlier double-quote escaping survives into the later vulnerable helper, supporting the explicitly reported CVE-2023-40581/2024-22423 bypass lineage without issue-count inflation. Old selected shell_quote production calls format diagnostics while q-format calls compat_shlex_quote directly; newly wired consumers do not establish an old selected-helper sink. Smuggled preexisting headers override internal referrer additions and become privileged proxy routing in Vimeo/Generic; Vimeo destination restrictions and HTTPS/Secure-cookie consequences remain qualified. Native redirect Cookie filtering precedes the downloader-boundary repair; the latter still has an old fragment first-request witness, not a newly unpatched native redirect. Scoped-cookie producer/native/external adapters are coordinated. An all-headers-removed None shape conflicts with a fragment copy consumer, but old standalone admission remains unestablished; preserve that open compatibility question and withhold a complete standalone negative. Preserve all831 discovery events, six supported/one ambiguous statuses and all prior authored history. CPython3.11.4 is a comparison, not deployment proof. Retained programs, requests, payloads and upstream tests remain inert.',
                       '- Thirty-second batch: all six remaining Cookiecutter candidates/four mechanical families, completing all nine repository rows/five families. Two defer missing context, three selected attribution and one paired negative. Locale-default decoding can corrupt admitted UTF-8 JSON/default values before parsing, while ordinary old hook producers correctly return status through matching wrappers and consumers; their exception migration does not isolate three old local failures. Prompt display suppression adds a Click7-only show_choices keyword while exact old/after setup still admits Click5+. Retained Click5.0/6.7 signatures reject it before ordinary interactive selection, introducing a supported after-contract compatibility failure. Append one ambiguous null-category revision withdrawing blanket display-only exclusion, without inventing a non-style old duplicate-display positive. Mercurial checkout revision data can become early config/debugger control despite argv use; after -- bounds that Hg route, not Git/clone URL/all template safety. Actual lower-trust API admission and installed versions remain conditional. Preserve all831 prefix events, all prior batches including the three batch004 proposals, source hashes and45 protected inputs. Comparisons and findings are inert source deductions; no retained programs, payloads, requests or upstream tests execute.',
                        '- Thirty-third batch: all six OpenStack Swift training candidates/one mechanical family. Two readers defer missing context, three constructor/writer components defer selected attribution and middleware defers its paired negative. Cache-controlled flags/bytes reach cPickle object construction conditionally on actual cache write/response control and reader invocation; public tenant object access alone does not establish that authority. Single get checks the hashed response key, while bulk get decodes rows before requested-key filtering; complete literal production retrieval finds no bulk caller beyond definitions, so public API tests do not establish an installed bulk service path. New policy-state and JSON-writing components are coordinated, not three independent old security defects. Exact ConfigParser/PasteDeploy text plus advertised Python2.6 mixed-type ordering makes textual modes0/1 disable both pickle flags, breaking documented legacy-cache migration. Missing settings use integer2 correctly; programmatic integer0/1 deliberately remain insecure. Record the introduced compatibility failure without inventing a Python3 crash or permissive unpickle bypass. Preserve all832 discovery events, two supported/four ambiguous statuses, prior batches and protected inputs. Four pinned evidence files retain64 inert texts/four archive peers; historical runtime/protocol comparisons are not deployment proof. No retained programs, payloads, vulnerability requests or upstream tests execute.',
                        '- Thirty-fourth batch: all six pysaml2 training candidates/one mechanical family. Three defer missing context and three selected security delivery. Historical CPython2.7.12/3.5.2 ElementTree comparisons support internal entity expansion before class/SOAP/signature checks, not the advisory arbitrary-file-read claim for these bindings. Generic SAML, SOAP typed extraction and class-instance/ECP parsing have matched old consumers; raw extension, pack parser and envelope opener do not inherit those sibling network paths. Literal src/example and wrapper retrieval establishes only their public API/wrapper evidence, not deployed lower-trust delivery or dynamic-call completeness. Defusedxml0.4.1/0.5.0 defaults reject declared entities before feed, but forbid_dtd=False is not all-DTD rejection or universal resource/signature/xmlsec safety. Pure/accelerated tree differences alone are not a supported after regression. Comparisons and the unversioned dependency do not certify installed/all future versions. Four pinned evidence files retain136 inert texts/six exact archive peers; preserve all832 ledger events, six supported statuses/categories, prior batches and45 protected inputs. Six functions are not independent issues; all retained programs, XML payloads, vulnerability requests and upstream tests stay inert.',
                        '- Thirty-fifth batch: all six Sydent training candidates/five mechanical families. Four defer missing context and two paired negatives. Configured TLS paths need peer verification, accepted client secrets lack a length bound, and HTTP GET/ignored POST bodies accumulate remote data before parsing/discard. Matched finite5KiB/50KiB GET callers and zero-size POST reader bound accumulation without zero-transient-memory, immediate-abort or universal-resource guarantees. Authenticated invitation sender is unbound to account identity; after equality narrows that authority, but default matrix-org/vector-im templates request bracketed_verified_sender_for_html while renderer generates _forhtml, introducing ordinary invitation failure before SMTP. The2019 raw-address forwarding still reaches smtplib quoteaddr/parseaddr under CPython2.7.16, retaining the validation/delivery identity mismatch. Later2.7.17 parser rejection and2021 Sydent equality checks are not backfilled into2019. Append one supported revision2 resolving prior2019 ambiguity with matched session/consumer/runtime evidence while explicitly deferring its residual after negative; preserve all832 prefix bytes and original category/hashes/family. Domain policy belongs to the historical Synapse consumer comparison, not an invented Sydent setting or deployed-version proof. Four pins retain145 inert texts/ten archive peers and explicit404 inventories. Six rows/five families are not independent issues; all retained programs, messages, payloads, requests and upstream tests stay inert.',
                         '- Thirty-sixth batch: all six pyload training candidates/five mechanical families. Four defer missing context, one selected attribution and one paired negative. New global anti-framing policy does not establish an old selected error-handler registrar duty or concrete framed action. API/UI login raw usernames reach configured line-oriented handlers on authentication failure; after escapes CR/LF in those two messages, not every log/control character. Origin TLS peer verification defaults on after but configurable False and unchanged HTTPS-proxy verification remain distinct. Redirect fallback endpoint changes correctly with its caller, yet login_required drops required route arguments: get_file cannot build without path and successful authentication falls back to dashboard instead of returning to the old protected file URL. Record the introduced return-destination integration regression and defer its paired negative. SameSite Strict bounds cross-site ambient admin-cookie delivery to state-changing GET under matched extension/browser/TLS policy, not same-site actors or general CSRF. Seven pins retain199 inert texts/twelve archive peers and three explicit404 requests; dependency and current URL-standard comparisons are not deployed browser/runtime proof. Preserve all833 discovery events, statuses/categories/hashes/families, prior batches and45 protected inputs. Six functions/five families are not independent issues; all retained programs, payloads, vulnerability requests and upstream tests stay inert.',
                         '- Thirty-seventh batch: all six markdown-it-py training candidates/two mechanical families. One defers missing context, four selected attribution and one paired negative. Standard core inline producers populate child lists, and ordinary image producer supplies alt; old recursive helper already accepts None at entry. Only its recursive nested-image assertion has the established standard producer witness, requiring assertions enabled and actual lower-trust Markdown rendering. Four companion guards do not become four independent old availability defects. CLI strict locale decoding can abort a batch, but malformed-byte tolerance and actual security delivery remain unestablished. After forced UTF8-ignore silently drops valid old cp1252 locale text, introducing a data-preservation regression; defer its paired negative without inventing an old security positive. CLI parent already contains the earlier renderer guards, so preserve version-specific contracts. Three pins retain134 inert texts/eight exact archive peers, two resolved parents/four archive inventories and explicit absent paths; CommonMark0.30 and CPython3.9.16 are semantic comparisons, not deployment/all-version proof. Preserve all833 discovery events, statuses/categories/hashes/families, prior authored batches and45 protected inputs. Six functions/two families are not independent issues; no retained programs, payloads, vulnerability requests or upstream tests execute.',
                          '- Thirty-eighth batch: all six LangChain training candidates/four mechanical families. Two defer missing context, one selected attribution and three paired negatives. Matched recursive HTTP consumers establish conditional raw-prefix authority escape, but after path-only relative joining loses query pagination. File-store key confinement uses different root/child normalization and rejects ordinary keys for legitimate roots containing parent segments. XML nonstreaming/async declaration paths differ from old sync pre-root stripping; Expat limits qualify expansion consequences, and standard ElementTree is not arbitrary external-file XXE. After removes SQL-cell eval but raw SQLAlchemy2.0 Row breaks the documented named-column retriever. Three introduced after-contract regressions are not new old security positives. Four pins retain120 inert texts/eight archive peers; preserve all833 discovery events and prior authored history. No retained programs, payloads, vulnerability requests or upstream tests execute.',
                          '- Thirty-ninth batch: all five TensorFlow training candidates/two mechanical families, including the null-category serializer exclusion. One proposes coordinated nonrepair exclusion, one defers intentional YAML-reader retirement task scope and three defer lock security delivery. Actual YAML after raises unconditionally despite safe_load-oriented commit title; loader constructs Python objects before Keras custom-object mapping, whereas serializer is not that sink. Declared API retirement is not an accidental after regression or preserved YAML roundtrip. Old constructor/restorer/lower-trace primitive locks can block finite same-thread recursive callbacks, but SavedModel lacks original Python code and does not itself establish that callback or pickle-restorer delivery. After RLock removes same-thread reacquisition blocking, not all recursion/resource/cross-thread/graph/model risks. Three pins retain56 inert texts/eight exact archive peers/two resolved parents/two explicit404 requests. Historical CPython/PyYAML/policy comparisons are not installed/all-version proof; explicit path retrieval is not exhaustive dynamic integration search. Preserve all833 ledger events, statuses/categories/hashes/families, prior authored history and45 protected inputs. Five functions/two families are not independent issues; no retained programs, payloads, vulnerability requests or upstream tests execute.',
                           '- Fortieth batch: all five Twisted training candidates/two mechanical families. Two defer missing context, two selected attribution and one security delivery. New redirect-constructor policy is coordinated with the actual origin filter; custom ETag capitalization mismatches Headers special canonical output, a new-option limitation without an old selected custom-policy duty. Broad header strip hides non-OWS framing octets and chunk int accepts non-RFC forms; after coordinated strict consumers reject witnessed forms. RFC nonconformance alone does not establish actual multi-parser desynchronization. Obs-fold change lacks an isolated meaning-changing old selected witness, and standalone fromChunk has no retained production caller. Four pins retain52 inert texts/four peers; the initial HTTP301 body is retrieval provenance only, and a separately retained redirect-following TLS-verified RFC7230 text supplies grammar evidence. Preserve all833 ledger events and earlier authored history; no retained programs, payloads, vulnerability requests or upstream tests execute.',
                           '- Forty-first batch: all five Saleor training candidates/three mechanical families, including two null categories. Three defer missing context, one proposes nonrepair exclusion and one defers security delivery. Empty explicit optional String selects an ambient refresh cookie while caller skips CSRF; matched csrf_exempt form-POST route and Secure/SameSite=None setter establish conditional cookie-authorized action, not automatic response-token theft. Browser third-party policy and DEBUG Lax remain qualified. Cleaner already rejects empty actual tokens and only coordinates changed missing/invalid classification. Fixed/input-derived JWT setup errors do not establish another-user secret disclosure or inherit the separately sanitized generic formatter; all-subclass typed-error enum compatibility is not certified. MANAGE_USERS without MANAGE_ORDERS admits another customer root, whose old orders callback filters drafts but not ownership; nested/outer copies are one overlapping path. Four pins retain149 inert texts/six exact peers/three resolved parents and explicit absent paths. Preserve all833 ledger events, source/dependence and45 protected inputs; comparisons are not installed/all-version proof and no retained programs, payloads, vulnerability requests or upstream tests execute.',
                           '- Forty-second batch: all four Keystone training candidates/three mechanical families. Two defer missing context, one residual paired negative and one security delivery. Old disabled-user update leaves embedded token snapshots; current-user lookup closes new token minting even when companion revocation cannot enumerate tokens. That after-selected text equals the next expiry-before positive and still resets parent lifetime through the matched default creator: preserve an explicit residual after-contract deferral, not an introduced regression or whole-function clean negative. Next repair carries finite parent expiry; explicit None is an old nonexpiry state. Last-role removal clears tenant membership/revokes tokens, but valid EC2 signatures still reissue a scoped identity accepted by Keystone validation; inherited S3 is the same mechanism and downstream zero-role operations remain policy-dependent. Existing DEBUG startup config dump plus admitted oslo.config1.1.0 sanitizer establishes secret-flag repair for admin_token/ldap.password, while less-authorized log readership remains unresolved. Three pins retain219 inert texts/eight peers/four parents/eight archive inventories and absent-path provenance. Selected-after/before equality is not full-file equality or parent adjacency. Preserve all833 discovery events and prior authored history; no retained programs, payloads, vulnerability requests or upstream tests execute.',
                           '- Forty-third batch: all four pyoidc training candidates/one mechanical family, including the null-category message-helper exclusion. One defers security delivery, one selected attribution and one a residual paired negative; one proposes nonrepair exclusion. Old claim-verifier installed lower-trust invocation is not established by the newly added Consumer call. Wrapper forwards new flow context to a new guard rather than dropping an existing parameter. Consumer adds expected algs/final verification, yet _parse_authz discards kwargs and the saved-code exception lacks actual Token Endpoint provenance: unsigned callback ID claims can still return under matched request/state/nonce assumptions. Bare ID-token acceptance is residual, not invented introduction; later valid-code requirements may stop application login. Message helper relaxes none hashes and delegates policy, not a separate local security repair; adjacent IdToken time checks belong to another method. Three pins retain54 inert texts/six exact peers/one resolved first parent/two archive inventories and explicit missing paths. OIDC1.0 errata1-2014 and admitted pyjwkest1.4.2 are comparisons, not deployment/all-version proof. Preserve all833 ledger events, prior authored evidence and45 protected inputs; four functions/one family are not independent issues and no retained programs, payloads, vulnerability requests or upstream tests execute.',
                            '- Forty-fourth batch: all four urllib3 training candidates/four mechanical families, including the null-category mislinked percent-normalization exclusion. Two defer missing context, one a residual paired negative and one proposes nonrepair exclusion. Matched Retry/header/origin contracts establish the case-insensitive configured-header repair, but exact 2018 after still preserves private replayable bytes through a cross-origin 303 GET transition; named old transport sends that body, so preserve a residual after-contract deferral without claiming selected equality or direct adjacency to 2023. The later manager repair explicitly clears body and prepares content headers. Selected percent pair introduces its helper and lacks the advisory-described later repeated-replace loop; resolved 1.25.7/1.25.8 show the later loop-to-subn comparison. Old Python3 tests already expect binary URL rejection, not a newly introduced supported-input regression. Greedy subauthority partitioning is a separate CPU mechanism; rpartition plus host-only regex removes repeated partitions, but expanded patterns/runtime/caller limits remain contextual. A standard redirect join can reject unmatched brackets before this parser; direct initial URL parsing is a different path. Four pins retain186 inert texts/eight exact peers/four parents/eight archive inventories. Preserve all833 ledger events, prior authored evidence and45 protected inputs; four functions/four families are not independent issues, historical comparisons are not deployment/all-version proof and no retained programs, payloads, vulnerability requests or upstream tests execute.',
                            '- Forty-fifth batch: all four bcfg2 training candidates/one mechanical family. One defers missing context, one security delivery and two paired negatives. Actual Basic-auth/global-password/default-profile/session metadata chain establishes conditional client name influence, not anonymous root, arbitrary aliases or all first-time cached-certificate paths. Selected signing command has server-config/temp operands and cannot inherit sibling request-key injection. Its matched after request helper changes to a list but keeps shell=True, so POSIX semantics invoke bare openssl, breaking the old certificate-generation contract before signing; record introduced integration failure without inventing an old selected security positive. Key verifier quotes paths but is gated by prior CA verification; do not borrow execution/output spoofing at that sibling sink as an independent selected delivery proof. CA verifier has its own cached hostname-path shell sink and after shell-free argv repair. SSHbase fixes DNS-error fallback shell interpretation but retains getent split-list output consumed by an address set; named IPv4-only Python/IPv6-capable getent comparisons establish ordinary successful fallback whose address is silently omitted. Record that failure as residual, not introduced or another security issue. Four pins retain60 inert texts/four exact peers/one resolved first parent/two archive inventories and missing paths. Maintenance backport has a different file set without SSLCA, so no automatic repair/alias equivalence. Preserve all833 ledger events, prior authored evidence and45 protected inputs; four functions/one family are not independent issues and no retained programs, payloads, vulnerability requests or upstream tests execute.',
                             '- Forty-sixth batch: all four OpenStack swauth training candidates/one mechanical family. Three defer missing context and one a residual paired negative. Old issuance, local cache-miss group lookup and external validation embed live bearer token-object names in backend URIs; named Swift2.15.0 request/object logging supports conditional log-reader replay independently of token-header truncation. Coordinated after uses prefix:token:suffix SHA512 hexadecimal names and digest-derived shard under the advertised Python2.7 shape, not an invented Python3 regression. User deletion has a distinct conditional live-cache witness after successful object/user DELETE without a failed-delete race. Both exact handlers omit token-cache invalidation while matched readers accept unexpired groups and authorize without a user/object recheck; record that ordinary revocation failure as residual and defer its paired negative, preserving ambiguous discovery history. Front-door/remote validation URIs and auth posthook path logs remain outside the repaired backend-name negative; no complete secret-log certification. Commit-announced old-token logout without memcached is intentional transition context, not accidental regression or automatic migration proof. Four pins retain47 inert texts/two exact peers/one resolved first parent/two archive inventories and requested-missing provenance. Named dependencies are not installed/all-version/deployed proof. Preserve all833 ledger events, prior authored evidence and45 protected inputs; four functions/one family are not independent issues and no retained programs, payloads, vulnerability requests or upstream tests execute.',
                             '- Forty-seventh batch: all four qutebrowser training candidates/three mechanical families. One defers missing context and three paired negatives. Accepted certificate exception plus reset/no-new-callback can mislabel a successful reload; new shared host set fixes the remembered top-level case but loses the old warning for an accepted certificate error on a different-host subresource. Privileged settings mutation lacks request binding; new backend/token/template guards add it, yet each render overwrites one process-global token and invalidates earlier normal settings pages. Matched WebKit caller supplies the new method/current-tab arguments correctly; its canonical gate is locally bounded and the downstream token-lifetime failure stays attributed to its settings owner, not another independent guard defect. Stored website title reaches innerHTML after JSON parsing; title escaping repairs markup, but after also HTML-escapes URL data assigned directly to DOM href, turning valid query delimiters into literal entity text and changing navigation. Three introduced ordinary after-contract regressions require explicit paired-negative deferral; do not invent a missing-password/None bypass, None-title crash, silent first-visit TLS bypass or automatic editor execution. Four pins retain228 inert texts/eight exact peers/three resolved parents/six archive inventories with missing/redirect provenance. Qt/Python/HTML historical comparisons are not installed/all-version/deployed proof; W3C text was retrieved with TLS-verified curl after Python CA validation failure. Preserve all833 ledger events, prior authored evidence and45 protected inputs; four functions/three families are not independent issues and no retained programs, payloads, vulnerability requests or upstream tests execute.',
                              '- Forty-eighth batch: all four cloud-init training candidates/three mechanical families. Three defer missing context and one selected attribution. Old metadata policy/redaction/public JSON establishes privacy duty, but known lower-case Vultr user/vendor fields require new policy entries rather than proving an isolated old case-normalization miss; preserve ambiguous classifier discovery. LXD after extends defaults while retaining dotted keys, and JSON-roundtripped keys are strings. Old RANDOM passwords go to stderr and the default tee pipe; matched service/tee/POSIX contracts support conditional new0644 output files. After child umask0037/optional adm GID bounds new pipe-created modes, while a companion writer separately moves passwords to console. Old non-strict boot schema warnings include repr-bearing validator errors; after exact boot caller suppresses details without retiring default/strict CLI diagnostics. Main FileHandler can create0644 before initialization; old preserve_mode retains it despite requested0640 and after False enforces mode through empty append/chmod without truncation. Old Vultr DEBUG output supplies a concrete conditional secret writer. Keep output-log/main-log/public-JSON sinks and2021/2022/2023 lineages distinct; shared disclosure context is not independent issue adjudication. Three pins retain359 inert texts/eight exact peers/three resolved parents/six archive inventories and missing provenance; historical validator/runtime/service/utility contracts are not installed/all-version/deployed proof. Preserve all833 ledger events, prior authored evidence and45 protected inputs; no retained programs, payloads, vulnerability requests or upstream tests execute.',
                              '- Forty-ninth batch: all four rdiffweb training candidates/four mechanical families. Three defer missing context and one a residual paired negative. Old password changes leave username-bound sessions authenticated; after deletes other rows and matched caller commits, but another already-loaded ID can be reinserted by unchanged DbSession save-on-missing behavior. Per-ID locks and named CherryPy/SQLAlchemy/pysqlite contracts support a conditional loaded-session resurrection schedule, not an introduced regression or an all-isolation claim. Admin GET deletion reaches real store DELETEs despite username validation; Lax permits admitted safe top-level navigation and old Origin guard skips GET. After submission gate preserves actual POST modal but is not universal CSRF repair. Earlier current-password reauthentication already exists; after counts five failed checks per session and clears/regenerates before login redirect, with matched required-field/helper/admin API contracts and no invented keyword regression. Later generic rate-limit decorator is not backfilled. Origin prefix admits a different authority; actual profile mutation plus same-site hostile delegated prefix hosting can preserve Lax credentials, unlike arbitrary cross-site POST. Exact supplied-Origin equality repairs that witness, not missing-Origin/Referer/proxy/CORS/all CSRF. Five pins retain373 inert texts/eight exact peers/four resolved parents/eight archive inventories and nine requested missing paths, with proper helpers resolved separately. Historical runtime/framework/validator/database/browser comparisons are not installed/all-version/deployed proof; IETF HTTPS text used TLS-verified curl after Python CA validation failure. Preserve all833 ledger events, prior authored evidence and45 protected inputs; functions/families are not independent issues and no retained programs, payloads, vulnerability requests or upstream tests execute.',
                  '- Narrow mechanism descriptors are retained without forcing them into existing leaves with incompatible boundaries. Final eligibility, context protocol, security placement and independent issue counts remain pending.', '',
               '| Assistant subset proposal | Candidates |', '|---|---:|']
    report += [f'| {proposal} | {count} |' for proposal, count in reviews['proposal_counts'].items()]
    report += ['', '## Student-approved selection principles — 1 November2026', '',
                 'The student approved equal function-only inputs, genuine existing bugs, credible security labels, defensible fixed counterparts, underlying-issue grouping and broad reporting categories with detailed traceability. See EXPERIMENT_SELECTION_DECISIONS.md for the supervisor note, next steps and publishing plan. This is policy approval, not blanket case-level label/subset/category/issue approval; the numerical input limit and ordinary-knowledge rule still need specification. Final subset size and adequacy for model development/evaluation remain unknown.', '',
                 '## Completed training coverage and approval handoff', '',
                            'All742 training candidates now have current assistant consolidation proposals, with0 remaining and0 stale reviews. The immutable051–059 schedule is complete: eight groups of ten and the final singleton, covering every discovery status and null category in each selected repository queue. Batches055–059 add41 candidates:25 context,3 existing-contract,6 paired-negative,4 security-boundary and3 selected-attribution deferrals. The exact locked TarSafe0.0.3 still checks CWD rather than extraction root, so Rasa retains an explicit residual paired-negative failure; see CATEGORY_AUDIT_CONSOLIDATION_REVIEW.md for full findings and fingerprints. Preserve existing IDs/source bytes/splits, narrow contracts, bounded negatives, nested/coordinated representations and dependence. Operational rows/families are not independent issues. Coverage completion does not approve eligibility or freeze the experiment. Evidence stays inert and adjudication-only; researcher confirmation and the common before-only budget/ordinary-knowledge policy remain pending.', '',
                 '1. Resolve recorded eligibility exceptions using retained source/fix evidence; record any changed discovery decision as an appended ledger revision, not an edit.',
               '2. Review exact-version/overlap links and explicit follow-up chains; retain separate root causes within conservative dependence blocks until adjudicated.',
               '3. Complete the common before-only input/observability and paired-negative decisions using `CATEGORY_AUDIT_CONSOLIDATION_REVIEW.md`; no context or eligibility is certified by cue counts.',
               '4. Resolve actual dependency/caller contracts and any missing evidence pins that earlier notes leave open. Retained supplemental files are hash-verified, not certified as sufficient.',
               '5. Prepare researcher confirmation only after coherent taxonomy/eligibility/context/issue proposals and explicitly bounded exceptions exist. No freeze or held-out category adjudication yet.', '',
               '## Reproduce', '', '```sh', 'python3 CATEGORY_AUDIT_CONSOLIDATE.py build',
               'python3 CATEGORY_AUDIT_CONSOLIDATE.py check', 'python3 CATEGORY_AUDIT.py check', '```', '',
               f"The consolidation manifest fingerprints its source plan, taxonomy, complete ledger, tooling, review protocol, {len(SUPPLEMENTAL_PINS)} supplemental evidence files and generated artifacts. It verifies {supplemental['embedded_source_count']} embedded source-text digests plus the standalone enum template against the previously recorded pins. Hash preservation does not establish deployed dependency versions or complete caller contracts. The protected release/input lock is unchanged.", '']

    result = {
        OUTPUTS['crosswalk']: json_text(dict(version=plan['version'], status=plan['status'],
            scope='training_only', source_taxonomy_version=definitions['version'], rules=plan['rules'],
            parents=plan['parents'], mappings=crosswalk, priority_boundary_reviews=plan['priority_boundary_reviews'])),
        OUTPUTS['queue']: ''.join(json.dumps(record, ensure_ascii=False, separators=(',', ':'))+'\n' for record in work),
        OUTPUTS['dependence']: json_text(dependence), OUTPUTS['counts']: stream.getvalue(),
        OUTPUTS['report']: '\n'.join(report), OUTPUTS['reviews']: json_text(reviews),
    }
    source_names = [PLAN, 'CATEGORY_AUDIT_CONSOLIDATE.py', 'CATEGORY_AUDIT_CONSOLIDATION_REVIEW.md',
                    'EXPERIMENT_SELECTION_DECISIONS.md',
                    'EXPERIMENT_PROTOCOL_DRAFT.md',
                    'CATEGORY_AUDIT_CONSOLIDATE_TEST.py',
                    'CATEGORY_AUDIT.py', 'CATEGORY_AUDIT_CATEGORIES.json', 'CATEGORY_AUDIT_LEDGER.jsonl',
                    'CATEGORY_AUDIT_INPUTS.json', *SUPPLEMENTAL_PINS, *REVIEW_BATCHES]
    manifest = dict(version=plan['version'], status=plan['status'], created=plan['created'],
        scope='training_only', researcher_approval_ready=False, training_candidates=len(train), ledger_events=len(events),
        discovery_ledger_prefix=dict(events=DISCOVERY_PREFIX_EVENTS, sha256=DISCOVERY_PREFIX_SHA256),
        protected_input_count=len(audit.load('CATEGORY_AUDIT_INPUTS.json')['sha256']),
        source_sha256={name: audit.file_sha(audit.ROOT/name) for name in source_names},
        output_sha256={name: audit.sha(text) for name, text in result.items()},
        supplemental_evidence_verification=supplemental,
        consolidation_reviewed_candidates=reviews['current_reviewed_candidates'],
        source_read_policy='Canonical held-out bytes are verified for integrity; all substantive derivation uses training projection only.',
        independently_adjudicated_issue_count=None)
    result[OUTPUTS['manifest']] = json_text(manifest)
    return result


def build_or_check(check=False):
    result = artifacts()
    for name, text in result.items():
        path = audit.ROOT/name
        if check:
            assert path.exists() and path.read_bytes() == text.encode(), f'Stale or missing consolidation artifact: {name}'
        else:
            path.write_bytes(text.encode())
    print(json.dumps(dict(command='check' if check else 'build', training_candidates=742,
        discovery_leaves=113, proposed_parents=len(audit.load(PLAN)['parents']),
        generated_artifacts=len(result), researcher_approval_ready=False,
        message='Consolidation artifacts are reproducible; protected inputs unchanged.' if check else 'Consolidation proposal saved.'), indent=2))

def training_inputs():
    protected = audit.protected_inputs()
    assert protected == audit.load('CATEGORY_AUDIT_INPUTS.json')['sha256']
    # Canonical/split verification may read held-out bytes for integrity only.
    # All subsequent taxonomy/statistics/links consume this training-only projection.
    train = {pid: row for pid, row in audit.dataset().items() if row['split'] == 'train'}
    families = audit.components(train)
    events, latest = audit.ledger(train, families)
    assert len(train) == len(latest) == 742 and len(events) >= DISCOVERY_PREFIX_EVENTS
    prefix = (audit.ROOT/'CATEGORY_AUDIT_LEDGER.jsonl').read_bytes().splitlines(keepends=True)[:DISCOVERY_PREFIX_EVENTS]
    assert audit.sha(b''.join(prefix)) == DISCOVERY_PREFIX_SHA256, 'Completed discovery ledger prefix changed'
    assert set(train) == set(latest)
    assert {row['issue_group'] for row in train.values()} <= {'security_candidate', 'correctness_candidate'}
    return train, families, events, latest


def inventory():
    train, families, events, latest = training_inputs()
    print('TRAINING RECORD KEYS', sorted(next(iter(train.values()))))
    print('DOMAINS', Counter(c['domain'] for c in audit.load('CATEGORY_AUDIT_CATEGORIES.json')['categories']))
    for category in audit.load('CATEGORY_AUDIT_CATEGORIES.json')['categories']:
        chosen = [pid for pid, event in latest.items() if event['category_id'] == category['category_id']]
        supported = [pid for pid in chosen if latest[pid]['review_status'] == 'assistant_supported']
        print(category['category_id'], dict(Counter(latest[pid]['review_status'] for pid in chosen)),
              'supported_families', len({families[pid] for pid in supported}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['inventory', 'build', 'check'])
    args = parser.parse_args()
    if args.command == 'inventory':
        inventory()
    else:
        build_or_check(args.command == 'check')
