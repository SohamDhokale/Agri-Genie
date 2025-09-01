from django.core.management.base import BaseCommand
from apps.schemes.models import GovernmentScheme

class Command(BaseCommand):
    help = 'Populate government schemes data'
    
    def handle(self, *args, **options):
        schemes_data = [
            {
                'name': 'Pradhan Mantri Fasal Bima Yojana (PMFBY)',
                'category': 'insurance',
                'description': 'Crop insurance scheme to provide insurance coverage and financial support to farmers in the event of failure of any of the notified crop.',
                'eligibility': 'All farmers including sharecroppers and tenant farmers growing notified crops in notified areas.',
                'benefits': 'Premium rates: 2% for Kharif, 1.5% for Rabi crops, 5% for annual commercial/horticultural crops.',
                'application_process': 'Apply through banks, insurance companies, or online portal.',
                'documents_required': 'Aadhaar card, land documents, bank passbook, sowing certificate.',
                'contact_info': 'Contact local agriculture office or visit pmfby.gov.in',
                'website_url': 'https://pmfby.gov.in'
            },
            {
                'name': 'PM-KISAN Samman Nidhi',
                'category': 'subsidy',
                'description': 'Direct income support scheme for small and marginal farmers.',
                'eligibility': 'Small and marginal farmer families having combined land holding/ownership of up to 2 hectares.',
                'benefits': 'Financial benefit of Rs. 6000 per year in three equal installments.',
                'application_process': 'Apply online or through Common Service Centers.',
                'documents_required': 'Aadhaar card, land ownership documents, bank account details.',
                'contact_info': 'Visit pmkisan.gov.in or contact local revenue official',
                'website_url': 'https://pmkisan.gov.in'
            },
            {
                'name': 'Kisan Credit Card (KCC)',
                'category': 'loan',
                'description': 'Credit facility for farmers to meet their cultivation and other needs.',
                'eligibility': 'All farmers including tenant farmers, oral lessees, sharecroppers.',
                'benefits': 'Flexible credit limit, lower interest rates, insurance coverage.',
                'application_process': 'Apply through banks with required documents.',
                'documents_required': 'Land documents, identity proof, address proof, passport size photos.',
                'contact_info': 'Contact nearest bank branch',
                'website_url': ''
            },
            {
                'name': 'Soil Health Card Scheme',
                'category': 'technology',
                'description': 'Promote soil health through judicious use of fertilizers.',
                'eligibility': 'All farmers',
                'benefits': 'Free soil testing and soil health card with nutrient recommendations.',
                'application_process': 'Contact local agriculture department.',
                'documents_required': 'Land ownership documents, farmer identification.',
                'contact_info': 'Local Krishi Vigyan Kendra or Agriculture Department',
                'website_url': 'https://soilhealth.dac.gov.in'
            },
            {
                'name': 'National Mission on Sustainable Agriculture (NMSA)',
                'category': 'technology',
                'description': 'Enhance agricultural productivity especially in rainfed areas.',
                'eligibility': 'All categories of farmers',
                'benefits': 'Funding for climate resilient technologies, capacity building.',
                'application_process': 'Through state agriculture departments.',
                'documents_required': 'Project proposal, farmer identification documents.',
                'contact_info': 'State Agriculture Department',
                'website_url': ''
            },
            {
                'name': 'Pradhan Mantri Krishi Sinchayee Yojana (PMKSY)',
                'category': 'subsidy',
                'description': 'Ensure access to irrigation water to every farm and improve water use efficiency.',
                'eligibility': 'All farmers, especially small and marginal farmers.',
                'benefits': 'Subsidy for micro-irrigation systems, water conservation structures.',
                'application_process': 'Apply through state agriculture departments or online portal.',
                'documents_required': 'Land documents, farmer ID, bank details, project proposal.',
                'contact_info': 'State Agriculture Department or PMKSY portal',
                'website_url': 'https://pmksy.gov.in'
            },
            {
                'name': 'National Agriculture Market (eNAM)',
                'category': 'technology',
                'description': 'Online trading platform for agricultural commodities.',
                'eligibility': 'All farmers, traders, and commission agents.',
                'benefits': 'Better price discovery, reduced transaction costs, transparent trading.',
                'application_process': 'Register online on eNAM portal.',
                'documents_required': 'Aadhaar card, bank account, mobile number.',
                'contact_info': 'Visit enam.gov.in or contact local APMC.',
                'website_url': 'https://enam.gov.in'
            },
            {
                'name': 'Pradhan Mantri Kisan Maan Dhan Yojana (PM-KMY)',
                'category': 'insurance',
                'description': 'Pension scheme for small and marginal farmers.',
                'eligibility': 'Small and marginal farmers aged 18-40 years.',
                'benefits': 'Monthly pension of Rs. 3000 after attaining 60 years of age.',
                'application_process': 'Apply through Common Service Centers or online.',
                'documents_required': 'Aadhaar card, land documents, bank account, age proof.',
                'contact_info': 'Visit pmkmy.gov.in or contact CSC centers.',
                'website_url': 'https://pmkmy.gov.in'
            },
            {
                'name': 'Agricultural Infrastructure Fund (AIF)',
                'category': 'loan',
                'description': 'Financing facility for investment in projects for post-harvest management.',
                'eligibility': 'Primary Agricultural Credit Societies, FPOs, entrepreneurs.',
                'benefits': 'Interest subvention of 3% per annum up to Rs. 2 crore.',
                'application_process': 'Apply through eligible lending institutions.',
                'documents_required': 'Project proposal, financial statements, land documents.',
                'contact_info': 'Contact eligible banks or financial institutions.',
                'website_url': ''
            },
            {
                'name': 'PM-FME (Food Processing)',
                'category': 'subsidy',
                'description': 'Support for food processing units and value addition.',
                'eligibility': 'Individual entrepreneurs, FPOs, cooperatives.',
                'benefits': 'Capital subsidy up to 35% for general areas, 50% for difficult areas.',
                'application_process': 'Apply through state food processing departments.',
                'documents_required': 'Project report, financial statements, land documents.',
                'contact_info': 'State Food Processing Department or PM-FME portal.',
                'website_url': 'https://pmfme.mofpi.gov.in'
            },
            {
                'name': 'National Mission for Horticulture Development',
                'category': 'subsidy',
                'description': 'Promote holistic growth of horticulture sector.',
                'eligibility': 'All farmers, especially small and marginal farmers.',
                'benefits': 'Subsidy for horticulture crops, protected cultivation, post-harvest management.',
                'application_process': 'Through state horticulture departments.',
                'documents_required': 'Land documents, farmer ID, project proposal.',
                'contact_info': 'State Horticulture Department',
                'website_url': ''
            },
            {
                'name': 'Pradhan Mantri Matsya Sampada Yojana (PMMSY)',
                'category': 'subsidy',
                'description': 'Comprehensive development of fisheries sector.',
                'eligibility': 'Fish farmers, fishermen, fish workers.',
                'benefits': 'Subsidy for fish farming, infrastructure development, insurance coverage.',
                'application_process': 'Apply through state fisheries departments.',
                'documents_required': 'Identity proof, land/water body documents, project proposal.',
                'contact_info': 'State Fisheries Department',
                'website_url': 'https://pmmsy.dof.gov.in'
            },
            {
                'name': 'National Livestock Mission',
                'category': 'subsidy',
                'description': 'Sustainable development of livestock sector.',
                'eligibility': 'Livestock farmers, dairy farmers, poultry farmers.',
                'benefits': 'Subsidy for livestock development, feed and fodder, insurance.',
                'application_process': 'Through state animal husbandry departments.',
                'documents_required': 'Farmer ID, livestock details, project proposal.',
                'contact_info': 'State Animal Husbandry Department',
                'website_url': ''
            },
            {
                'name': 'Pradhan Mantri Kisan Sampada Yojana (PMKSY)',
                'category': 'subsidy',
                'description': 'Comprehensive development of food processing sector.',
                'eligibility': 'Individual entrepreneurs, FPOs, cooperatives, companies.',
                'benefits': 'Capital subsidy for food processing units, cold chain infrastructure.',
                'application_process': 'Apply through Ministry of Food Processing Industries.',
                'documents_required': 'Detailed project report, financial statements, land documents.',
                'contact_info': 'Ministry of Food Processing Industries',
                'website_url': 'https://mofpi.gov.in'
            },
            {
                'name': 'National Mission for Sustainable Agriculture (NMSA) - Rainfed Area Development',
                'category': 'technology',
                'description': 'Improve productivity and sustainability of rainfed agriculture.',
                'eligibility': 'Farmers in rainfed areas.',
                'benefits': 'Support for integrated farming systems, soil conservation, water harvesting.',
                'application_process': 'Through state agriculture departments.',
                'documents_required': 'Land documents, farmer ID, project proposal.',
                'contact_info': 'State Agriculture Department',
                'website_url': ''
            },
            {
                'name': 'Pradhan Mantri Kisan Urja Suraksha evam Utthaan Mahabhiyan (PM-KUSUM)',
                'category': 'subsidy',
                'description': 'Solar power generation and irrigation pump solarization.',
                'eligibility': 'Individual farmers, cooperatives, panchayats.',
                'benefits': 'Subsidy for solar pumps, solar power plants on barren land.',
                'application_process': 'Apply through state renewable energy departments.',
                'documents_required': 'Land documents, farmer ID, electricity connection details.',
                'contact_info': 'State Renewable Energy Department',
                'website_url': 'https://pmkusum.mnre.gov.in'
            },
            {
                'name': 'National Mission on Oilseeds and Oil Palm (NMOOP)',
                'category': 'subsidy',
                'description': 'Increase production and productivity of oilseeds and oil palm.',
                'eligibility': 'Oilseed and oil palm farmers.',
                'benefits': 'Subsidy for seeds, fertilizers, plant protection, irrigation.',
                'application_process': 'Through state agriculture departments.',
                'documents_required': 'Land documents, farmer ID, crop details.',
                'contact_info': 'State Agriculture Department',
                'website_url': ''
            },
            {
                'name': 'Pradhan Mantri Kisan Samruddhi Kendras (PMKSK)',
                'category': 'training',
                'description': 'One-stop solution for farmers to access various agricultural services.',
                'eligibility': 'All farmers',
                'benefits': 'Access to quality inputs, advisory services, market linkages.',
                'application_process': 'Visit nearest PMKSK center.',
                'documents_required': 'Farmer ID, Aadhaar card.',
                'contact_info': 'Nearest PMKSK center or agriculture department.',
                'website_url': ''
            },
            {
                'name': 'National Mission on Agricultural Extension and Technology (NMAET)',
                'category': 'training',
                'description': 'Strengthen agricultural extension services and technology transfer.',
                'eligibility': 'All farmers',
                'benefits': 'Training programs, demonstrations, advisory services.',
                'application_process': 'Contact local Krishi Vigyan Kendra or agriculture office.',
                'documents_required': 'Farmer ID, contact details.',
                'contact_info': 'Local KVK or Agriculture Department',
                'website_url': ''
            },
            {
                'name': 'Pradhan Mantri Kisan Digital Mission',
                'category': 'technology',
                'description': 'Digital solutions for farmers to access information and services.',
                'eligibility': 'All farmers',
                'benefits': 'Digital advisory, market information, financial services.',
                'application_process': 'Register on digital platforms or mobile apps.',
                'documents_required': 'Aadhaar card, mobile number, bank account.',
                'contact_info': 'Visit digital agriculture portals or contact agriculture department.',
                'website_url': ''
            },
            {
                'name': 'Sub-Mission on Agricultural Mechanization (SMAM)',
                'category': 'equipment',
                'description': 'Promote farm mechanization and reduce drudgery in farming.',
                'eligibility': 'Individual farmers, FPOs, cooperatives.',
                'benefits': 'Subsidy for farm machinery and equipment.',
                'application_process': 'Apply through state agriculture departments.',
                'documents_required': 'Land documents, farmer ID, machinery details.',
                'contact_info': 'State Agriculture Department',
                'website_url': ''
            },
            {
                'name': 'Pradhan Mantri Kisan Seva Kendras',
                'category': 'training',
                'description': 'Service centers for farmers to access various agricultural services.',
                'eligibility': 'All farmers',
                'benefits': 'Quality inputs, advisory services, market information.',
                'application_process': 'Visit nearest service center.',
                'documents_required': 'Farmer ID, Aadhaar card.',
                'contact_info': 'Nearest Kisan Seva Kendra',
                'website_url': ''
            },
            {
                'name': 'National Mission for Protein Supplements',
                'category': 'subsidy',
                'description': 'Promote production of pulses and protein-rich crops.',
                'eligibility': 'Pulse and protein crop farmers.',
                'benefits': 'Subsidy for seeds, fertilizers, plant protection.',
                'application_process': 'Through state agriculture departments.',
                'documents_required': 'Land documents, farmer ID, crop details.',
                'contact_info': 'State Agriculture Department',
                'website_url': ''
            },
            {
                'name': 'Pradhan Mantri Kisan Credit Card - Animal Husbandry',
                'category': 'loan',
                'description': 'Credit facility for animal husbandry and dairy activities.',
                'eligibility': 'Livestock farmers, dairy farmers.',
                'benefits': 'Flexible credit limit, lower interest rates, insurance coverage.',
                'application_process': 'Apply through banks with required documents.',
                'documents_required': 'Livestock details, identity proof, address proof.',
                'contact_info': 'Contact nearest bank branch',
                'website_url': ''
            },
            {
                'name': 'National Mission on Agricultural Extension and Technology - ATMA',
                'category': 'training',
                'description': 'Agricultural Technology Management Agency for extension services.',
                'eligibility': 'All farmers',
                'benefits': 'Training programs, demonstrations, farmer field schools.',
                'application_process': 'Contact local ATMA office.',
                'documents_required': 'Farmer ID, contact details.',
                'contact_info': 'Local ATMA office or Agriculture Department',
                'website_url': ''
            }
        ]
        
        for scheme_data in schemes_data:
            scheme, created = GovernmentScheme.objects.get_or_create(
                name=scheme_data['name'],
                defaults=scheme_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Created scheme: {scheme.name}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Scheme already exists: {scheme.name}")
                )
        
        self.stdout.write(
            self.style.SUCCESS(f"Successfully processed {len(schemes_data)} schemes!")
        )
