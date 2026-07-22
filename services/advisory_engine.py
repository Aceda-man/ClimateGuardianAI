TRANSLATIONS = {
    "English": {
        "critical": "Multiple high-risk incidents reported in your area. Avoid affected zones and follow guidance from local authorities. Early community reporting is helping reduce exposure and response time.",
        "high": "Risk indicators are rising based on recent community reports. Stay alert, and continue reporting new incidents so your community's early warning stays accurate.",
        "moderate": "Conditions are stable but being actively monitored. Continued reporting helps strengthen early detection for your community.",
        "low": "No significant threats currently detected. Your community's reporting activity keeps this early warning system accurate and up to date.",
    },
    "Yoruba": {
        "critical": "Ọ̀pọ̀lọpọ̀ ìṣẹ̀lẹ̀ tó léwu ni wọ́n ròyìn ní àgbègbè yín. Yẹra fún àwọn agbègbè tó kan, kí ẹ sì tẹ̀lé ìtọ́ni àwọn aláṣẹ ìbílẹ̀.",
        "high": "Ewu ń pọ̀ sí i gẹ́gẹ́ bí àwọn ìròyìn titun láti àgbègbè yii. Ẹ máa ṣọ́ra, kí ẹ sì máa ròyìn ìṣẹ̀lẹ̀ tuntun.",
        "moderate": "Ipò náà dúró ṣinṣin ṣùgbọ́n a ń bójú tó o. Ìròyìn tí ẹ ń ṣe ń mú ìṣàwárí kíákíá lágbára sí i.",
        "low": "Kò sí ewu pàtàkì tí a ti rí lọ́wọ́lọ́wọ́. Ìròyìn àgbègbè yín ń jẹ́ kí ètò ìkìlọ̀ àkọ́kọ́ ṣiṣẹ́ dáadáa.",
    },
    "Hausa": {
        "critical": "An ba da rahoton abubuwan haɗari da yawa a yankinku. Ku guji wuraren da abin ya shafa, ku bi umarnin hukumomin gida.",
        "high": "Haɗari na ƙaruwa bisa rahotannin kwanan nan daga al'umma. Ku kasance a shirye, ku ci gaba da ba da rahoton sabbin abubuwan da suka faru.",
        "moderate": "Yanayin ya tsaya tsayin daka amma ana lura da shi sosai. Ci gaba da bayar da rahoto yana taimakawa gano matsaloli da wuri.",
        "low": "Babu wani babban haɗari da aka gano a yanzu. Ba da rahoto daga al'ummarku yana ci gaba da tabbatar da ingancin tsarin faɗakarwa da wuri.",
    },
    "Igbo": {
        "critical": "Ọtụtụ ihe ize ndụ ka a kọrọ na mpaghara gị. Zere ebe ndị metụtara, soro ntuziaka ndị ọchịchị mpaghara.",
        "high": "Ihe ize ndụ na-arị elu dabere na akụkọ ndị ọha na eze na nso nso a. Nọrọ na nchekwube, gaa n'ihu na-akọ ihe ndị ọhụrụ mere.",
        "moderate": "Ọnọdụ dị jụụ mana a na-elelịta ya nke ọma. Ịkọ akụkọ na-aga n'ihu na-enyere aka mepe ihe ndị ga-abịa n'oge.",
        "low": "Ọ dịghị ihe ize ndụ pụtara ìhè achọpụtara ugbu a. Akụkọ ọha na eze gị na-eme ka usoro ịdọ aka ná ntị mbụ dịgide.",
    },
}


def generate_advisory(risk, weather=None, language="English"):

    score = risk["score"]

    text = TRANSLATIONS.get(language, TRANSLATIONS["English"])

    if score >= 80:
        return {
            "icon": "🔴",
            "level": "Critical",
            "message": text["critical"]
        }

    elif score >= 50:
        return {
            "icon": "🟠",
            "level": "High",
            "message": text["high"]
        }

    elif score >= 20:
        return {
            "icon": "🟡",
            "level": "Moderate",
            "message": text["moderate"]
        }

    else:
        return {
            "icon": "🟢",
            "level": "Low",
            "message": text["low"]
        }