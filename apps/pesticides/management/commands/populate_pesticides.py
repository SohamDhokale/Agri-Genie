from django.core.management.base import BaseCommand
from apps.pesticides.models import Pesticide

class Command(BaseCommand):
    help = 'Populate pesticides data'

    def handle(self, *args, **options):
        pesticides_data = [
            {
                'name': 'Neem Oil',
                'category': 'insecticide',
                'active_ingredient': 'Azadirachtin',
                'description': 'Natural insecticide derived from neem tree seeds. Effective against a wide range of pests while being safe for beneficial insects.',
                'target_pests': 'Aphids, whiteflies, spider mites, mealybugs, scale insects, thrips',
                'application_method': 'Mix with water and spray on affected plants. Apply early morning or evening.',
                'dosage': '2-5 ml per liter of water',
                'safety_precautions': 'Wear gloves and eye protection. Avoid contact with eyes and skin. Keep away from children and pets.',
                'manufacturer': 'Organic Solutions Ltd.',
                'price_range': '₹200-500 per liter',
                'is_organic': True
            },
            {
                'name': 'Bacillus thuringiensis (Bt)',
                'category': 'insecticide',
                'active_ingredient': 'Bacillus thuringiensis var. kurstaki',
                'description': 'Biological insecticide containing naturally occurring soil bacteria that produce toxins lethal to certain insect larvae.',
                'target_pests': 'Caterpillars, cabbage loopers, tomato hornworms, corn earworms',
                'application_method': 'Spray on plant foliage where larvae are feeding. Apply when larvae are young.',
                'dosage': '1-2 grams per liter of water',
                'safety_precautions': 'Safe for humans and beneficial insects. Store in cool, dry place.',
                'manufacturer': 'BioControl Solutions',
                'price_range': '₹150-300 per 100g',
                'is_organic': True
            },
            {
                'name': 'Glyphosate',
                'category': 'herbicide',
                'active_ingredient': 'Glyphosate',
                'description': 'Systemic herbicide that kills weeds by inhibiting an enzyme essential for plant growth.',
                'target_pests': 'Broadleaf weeds, grasses, perennial weeds',
                'application_method': 'Spray directly on weed foliage. Avoid contact with desirable plants.',
                'dosage': '10-20 ml per liter of water',
                'safety_precautions': 'Wear protective clothing, gloves, and mask. Do not apply on windy days.',
                'manufacturer': 'CropCare Chemicals',
                'price_range': '₹800-1200 per liter',
                'is_organic': False
            },
            {
                'name': 'Copper Sulfate',
                'category': 'fungicide',
                'active_ingredient': 'Copper sulfate pentahydrate',
                'description': 'Fungicide used to control various fungal diseases in crops and prevent their spread.',
                'target_pests': 'Downy mildew, powdery mildew, blight, leaf spots',
                'application_method': 'Dissolve in water and spray on affected plants. Apply before disease appears.',
                'dosage': '2-4 grams per liter of water',
                'safety_precautions': 'Toxic to fish and aquatic life. Wear protective equipment. Do not apply near water bodies.',
                'manufacturer': 'Fungicide Solutions',
                'price_range': '₹300-600 per kg',
                'is_organic': False
            },
            {
                'name': 'Diatomaceous Earth',
                'category': 'insecticide',
                'active_ingredient': 'Silica (fossilized diatoms)',
                'description': 'Natural insecticide made from fossilized remains of diatoms. Works by damaging insect exoskeletons.',
                'target_pests': 'Ants, cockroaches, bed bugs, fleas, earwigs, silverfish',
                'application_method': 'Dust on soil surface or apply directly to insects. Reapply after rain.',
                'dosage': 'Apply thin layer on affected areas',
                'safety_precautions': 'Wear dust mask during application. Avoid inhaling dust particles.',
                'manufacturer': 'Natural Pest Control',
                'price_range': '₹200-400 per kg',
                'is_organic': True
            },
            {
                'name': '2,4-D Amine',
                'category': 'herbicide',
                'active_ingredient': '2,4-Dichlorophenoxyacetic acid',
                'description': 'Selective herbicide that controls broadleaf weeds without harming grasses.',
                'target_pests': 'Dandelions, clover, plantain, chickweed, thistles',
                'application_method': 'Spray on actively growing weeds. Avoid drift to desirable plants.',
                'dosage': '5-10 ml per liter of water',
                'safety_precautions': 'Wear protective clothing. Do not apply near sensitive crops or water bodies.',
                'manufacturer': 'WeedMaster Chemicals',
                'price_range': '₹600-900 per liter',
                'is_organic': False
            },
            {
                'name': 'Sulfur Dust',
                'category': 'fungicide',
                'active_ingredient': 'Elemental sulfur',
                'description': 'Traditional fungicide and miticide used for centuries to control plant diseases.',
                'target_pests': 'Powdery mildew, rust, scab, spider mites',
                'application_method': 'Dust on plant foliage or dissolve in water and spray.',
                'dosage': 'Apply thin layer or 2-4 grams per liter for spray',
                'safety_precautions': 'Wear dust mask and protective clothing. Avoid application in hot weather.',
                'manufacturer': 'Traditional Solutions',
                'price_range': '₹150-300 per kg',
                'is_organic': True
            },
            {
                'name': 'Pyrethrin',
                'category': 'insecticide',
                'active_ingredient': 'Pyrethrins (from chrysanthemum flowers)',
                'description': 'Natural insecticide derived from chrysanthemum flowers. Fast-acting contact insecticide.',
                'target_pests': 'Aphids, whiteflies, thrips, leafhoppers, beetles',
                'application_method': 'Spray directly on insects or affected plant parts.',
                'dosage': '5-10 ml per liter of water',
                'safety_precautions': 'Toxic to fish and bees. Apply in evening when bees are less active.',
                'manufacturer': 'Natural Insect Control',
                'price_range': '₹400-700 per liter',
                'is_organic': True
            },
            {
                'name': 'Atrazine',
                'category': 'herbicide',
                'active_ingredient': 'Atrazine',
                'description': 'Pre-emergent and post-emergent herbicide for control of broadleaf and grassy weeds.',
                'target_pests': 'Barnyard grass, foxtail, pigweed, ragweed, lambsquarters',
                'application_method': 'Apply to soil before weed emergence or spray on young weeds.',
                'dosage': '1-2 kg per hectare',
                'safety_precautions': 'Highly toxic to aquatic life. Wear protective equipment. Follow label instructions carefully.',
                'manufacturer': 'CropShield Chemicals',
                'price_range': '₹1200-1800 per kg',
                'is_organic': False
            },
            {
                'name': 'Mancozeb',
                'category': 'fungicide',
                'active_ingredient': 'Mancozeb (manganese + zinc + ethylene bisdithiocarbamate)',
                'description': 'Protective fungicide that prevents fungal spore germination and growth.',
                'target_pests': 'Early blight, late blight, downy mildew, leaf spots',
                'application_method': 'Spray on plant foliage before disease appears. Reapply every 7-10 days.',
                'dosage': '2-3 grams per liter of water',
                'safety_precautions': 'Wear protective clothing and mask. Do not apply within 7 days of harvest.',
                'manufacturer': 'Fungicide Pro',
                'price_range': '₹500-800 per kg',
                'is_organic': False
            },
            {
                'name': 'Spinosad',
                'category': 'insecticide',
                'active_ingredient': 'Spinosad (from soil bacterium)',
                'description': 'Natural insecticide derived from soil bacterium. Effective against many insect pests.',
                'target_pests': 'Caterpillars, thrips, leafminers, fruit flies, fire ants',
                'application_method': 'Spray on affected plants or apply as soil drench.',
                'dosage': '1-2 ml per liter of water',
                'safety_precautions': 'Toxic to bees. Apply in evening. Safe for humans and pets.',
                'manufacturer': 'BioInsect Solutions',
                'price_range': '₹800-1200 per liter',
                'is_organic': True
            },
            {
                'name': 'Paraquat',
                'category': 'herbicide',
                'active_ingredient': 'Paraquat dichloride',
                'description': 'Non-selective contact herbicide that kills green plant tissue on contact.',
                'target_pests': 'All green vegetation (non-selective)',
                'application_method': 'Spray directly on weeds. Avoid contact with desirable plants.',
                'dosage': '2-4 ml per liter of water',
                'safety_precautions': 'Highly toxic to humans. Wear full protective equipment. Do not inhale or ingest.',
                'manufacturer': 'Total Weed Control',
                'price_range': '₹1000-1500 per liter',
                'is_organic': False
            },
            {
                'name': 'Chlorothalonil',
                'category': 'fungicide',
                'active_ingredient': 'Chlorothalonil',
                'description': 'Broad-spectrum fungicide that prevents fungal diseases in various crops.',
                'target_pests': 'Powdery mildew, downy mildew, leaf spots, blights',
                'application_method': 'Spray on plant foliage. Apply before disease appears.',
                'dosage': '2-3 grams per liter of water',
                'safety_precautions': 'Wear protective clothing. Do not apply near water bodies. Toxic to fish.',
                'manufacturer': 'Fungicide Max',
                'price_range': '₹600-900 per kg',
                'is_organic': False
            },
            {
                'name': 'Garlic Oil',
                'category': 'insecticide',
                'active_ingredient': 'Allicin and sulfur compounds',
                'description': 'Natural insect repellent and mild insecticide derived from garlic.',
                'target_pests': 'Aphids, whiteflies, spider mites, mosquitoes',
                'application_method': 'Mix with water and spray on plants or use as repellent.',
                'dosage': '10-20 ml per liter of water',
                'safety_precautions': 'May cause skin irritation. Test on small area first. Strong odor.',
                'manufacturer': 'Organic Repellents',
                'price_range': '₹300-500 per liter',
                'is_organic': True
            },
            {
                'name': 'Bromoxynil',
                'category': 'herbicide',
                'active_ingredient': 'Bromoxynil',
                'description': 'Selective herbicide for control of broadleaf weeds in cereal crops.',
                'target_pests': 'Pigweed, ragweed, lambsquarters, kochia, Russian thistle',
                'application_method': 'Spray on actively growing weeds. Apply to cereal crops at specific growth stages.',
                'dosage': '0.5-1 liter per hectare',
                'safety_precautions': 'Wear protective clothing. Do not apply to non-target crops.',
                'manufacturer': 'Cereal Weed Control',
                'price_range': '₹800-1200 per liter',
                'is_organic': False
            }
        ]

        for pesticide_data in pesticides_data:
            pesticide, created = Pesticide.objects.get_or_create(
                name=pesticide_data['name'],
                defaults=pesticide_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Created pesticide: {pesticide.name}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Pesticide already exists: {pesticide.name}")
                )

        self.stdout.write(
            self.style.SUCCESS(f"Successfully populated {len(pesticides_data)} pesticides")
        )
