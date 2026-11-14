
from app import create_app
from models import db
from models.scheme import GovernmentScheme

app = create_app()


def seed_database():
    """Add default schemes without deleting existing database data."""
    with app.app_context():
        print("Preparing database...")
        db.create_all()

        schemes = [
            GovernmentScheme(
                name="Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)",
                ministry="Ministry of Agriculture and Farmers Welfare",
                description="PM-KISAN provides financial assistance of ₹6,000 per year to all landholding farmer families.",
                benefits="Direct income support of ₹6,000 per year in three installments.",
                eligibility="All landholding farmers' families in the country.",
                documents="Aadhaar Card, Land records, Bank details.",
                apply_link="https://pmkisan.gov.in/RegistrationFormupdated.aspx",
                category="Financial Support",
                is_state_specific=False,
                launch_year=2019
            ),
            GovernmentScheme(
                name="Pradhan Mantri Fasal Bima Yojana (PMFBY)",
                ministry="Ministry of Agriculture and Farmers Welfare",
                description="PMFBY provides insurance coverage and financial support to farmers in case of crop failure due to natural calamities.",
                benefits="Financial support to farmers suffering crop loss. Stabilization of income.",
                eligibility="All farmers growing notified crops in notified areas.",
                documents="Aadhaar Number, Land records (SOWING Certificate/RTC), Bank details.",
                apply_link="https://pmfby.gov.in/selfRegistration",
                category="Insurance",
                is_state_specific=False,
                launch_year=2016
            ),
            GovernmentScheme(
                name="Rashtriya Krishi Vikas Yojana (RKVY)",
                ministry="Ministry of Agriculture",
                description="RKVY aims at making farming a remunerative economic activity through strengthening the farmer's effort and risk mitigation.",
                benefits="Financial assistance for agriculture infrastructure and allied sector projects.",
                eligibility="Farmers, SHGs, and cooperatives involved in agriculture.",
                documents="Project proposal, Land records, Identity proof.",
                apply_link="https://rkvy.da.gov.in/",
                category="Technical Support",
                is_state_specific=False,
                launch_year=2007
            ),
            GovernmentScheme(
                name="National Mission on Oilseeds and Oil Palm (NMOOP)",
                ministry="Ministry of Agriculture",
                description="NMOOP aims to increase production of oilseeds and oil palm to reduce dependency on edible oil imports.",
                benefits="Subsidies for seeds, fertilizers, and technology adoption in oilseed cultivation.",
                eligibility="Farmers interested in oilseed or oil palm cultivation.",
                documents="Aadhaar Card, Land records, Bank Passbook.",
                apply_link="https://nfsm.gov.in/nfmis/NM_Login.aspx",
                category="Production Support",
                is_state_specific=False,
                launch_year=2014
            ),
            GovernmentScheme(
                name="Kisan Credit Card (KCC) Scheme",
                ministry="Ministry of Finance",
                description="KCC provides adequate and timely credit support from the banking system for cultivation and other needs.",
                benefits="Cheaper credit at low interest rates (4%) with flexible repayment.",
                eligibility="Owner cultivators, tenant farmers, and sharecroppers.",
                documents="Aadhaar Card, Identity proof, Address proof, Land cultivation proof.",
                apply_link="https://eseva.csccloud.in/KCC/default.aspx",
                category="Financial Support",
                is_state_specific=False,
                launch_year=1998
            ),
            GovernmentScheme(
                name="Soil Health Card Scheme",
                ministry="Ministry of Agriculture and Farmers Welfare",
                description="This scheme helps farmers understand soil health and use fertilizers appropriately.",
                benefits="A Soil Health Card indicates the nutrient status of farmers' land.",
                eligibility="Open to all farmers across the country.",
                documents="Soil samples are collected from the field.",
                apply_link="https://www.soilhealth.dac.gov.in/FARMER/FarmerRegistration",
                category="Technical Support",
                is_state_specific=False,
                launch_year=2015
            ),
            GovernmentScheme(
                name="e-NAM (National Agriculture Market)",
                ministry="Ministry of Agriculture and Farmers Welfare",
                description="e-NAM is a pan-India electronic trading portal connecting existing APMC mandis.",
                benefits="Unified national market and electronic auction for price discovery.",
                eligibility="Farmers, traders, and buyers who wish to trade agricultural commodities.",
                documents="Aadhaar Card, Bank Passbook, Mobile Number.",
                apply_link="https://www.enam.gov.in/web/register/farmer-registration",
                category="Marketplace",
                is_state_specific=False,
                launch_year=2016
            ),
            GovernmentScheme(
                name="Pradhan Mantri Krishi Sinchai Yojana (PMKSY)",
                ministry="Ministry of Jal Shakti",
                description="PMKSY aims to extend irrigation coverage and improve water-use efficiency.",
                benefits="Financial assistance for eligible micro-irrigation systems such as drip and sprinkler systems.",
                eligibility="Farmers meeting the applicable scheme and state requirements.",
                documents="Aadhaar Card, Land documents (RTC), Bank Passbook, Passport photo.",
                apply_link="https://pmksy.gov.in/",
                category="Technical Support",
                is_state_specific=False,
                launch_year=2015
            ),
            GovernmentScheme(
                name="E-Katha & Land Records (Karnataka)",
                ministry="Revenue Department, Government of Karnataka",
                description="Access digital records of land ownership, including RTC (Pahani), e-Katha, and mutation records.",
                benefits="Digital access to RTC and mutation reports to verify ownership and land details.",
                eligibility="All land owners and interested parties in Karnataka.",
                documents="Survey Number, District, Taluk, Hobli, Village.",
                apply_link="https://landrecords.karnataka.gov.in/service2/",
                category="Records",
                is_state_specific=True,
                state="Karnataka"
            )
        ]

        added = 0
        skipped = 0

        try:
            for scheme in schemes:
                existing = GovernmentScheme.query.filter_by(
                    name=scheme.name
                ).first()

                if existing:
                    skipped += 1
                else:
                    db.session.add(scheme)
                    added += 1

            db.session.commit()

            print(f"Seeding complete. Added: {added}. Already present: {skipped}.")
            print(
                f"Total schemes in database: "
                f"{GovernmentScheme.query.count()}"
            )

        except Exception as error:
            db.session.rollback()
            print(f"Could not seed schemes: {error}")
            raise


if __name__ == "__main__":
    seed_database()
