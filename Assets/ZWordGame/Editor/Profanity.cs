using System.Collections.Generic;

namespace ZWord.EditorTools
{
    /// <summary>
    /// Words that must never appear as level words or be rewarded as bonus words.
    /// Exact matches (after upper-casing). Extend freely; the baker re-runs when you save.
    /// </summary>
    public static class Profanity
    {
        // Profanity, slurs, sexual and drug terms, and words that read badly in a family-friendly game.
        static readonly string[] List =
        {
            "ANUS","ARSE","ARSES","ASS","ASSES","BASTARD","BASTARDS","BITCH","BITCHES","BITCHY","BOLLOCK","BOLLOCKS",
            "BONER","BOOB","BOOBS","BOOBIES","BOOTY","BUGGER","BUTT","BUTTS","CLIT","CLITS","COCK","COCKS","COON","COONS",
            "CRAP","CRAPS","CRAPPY","CUM","CUMS","CUNT","CUNTS","DAGO","DAGOS","DAMN","DAMNED","DICK","DICKS","DIKE","DIKES",
            "DILDO","DILDOS","DYKE","DYKES","FAG","FAGS","FAGGOT","FAGGOTS","FART","FARTS","FECES","FELLATE","FUCK","FUCKS",
            "FUCKED","FUCKER","FUCKERS","GOOK","GOOKS","GYP","GYPS","GYPPED","HELL","HOMO","HOMOS","HONKY","HONKIES","HOOKER",
            "HOOKERS","HORNY","JAP","JAPS","JIZZ","KIKE","KIKES","KILL","KILLS","KILLED","KILLER","LESBO","MURDER","NAZI","NAZIS",
            "NIGGER","NIGGERS","NIGGA","NIGGAS","ORGASM","ORGY","PECKER","PENIS","PENES","PERVERT","PISS","PISSED","PISSES",
            "POOP","PORN","PORNO","PORNS","PRICK","PRICKS","PUBES","PUBIC","PUSSY","PUSSIES","QUEER","QUEERS","RAPE","RAPED",
            "RAPES","RAPIST","RETARD","RETARDS","SCREW","SEMEN","SEX","SEXY","SEXES","SHAG","SHAGS","SHIT","SHITS","SHITTY",
            "SKANK","SLUT","SLUTS","SLUTTY","SMUT","SPAZ","SPIC","SPICS","SPERM","SUICIDE","TIT","TITS","TITTY","TITTIES",
            "TURD","TURDS","TWAT","TWATS","UTERI","VAGINA","VAGINAE","VAGINAS","VULVA","WANK","WANKER","WANKS","WETBACK",
            "WHORE","WHORES","WOP","WOPS","COKE","CRACK","METH","HEROIN","OPIUM","STONED","DOPE","BONG","BONGS","DRUNK",
            "NUDE","NUDES","NAKED","STRIP","STRIPS","EROTIC","LUST","LUSTY","BREAST","BREASTS","NIPPLE","NIPPLES","GAY",
            "GAYS","LEZ","LEZZES","TRANNY","MIDGET","MIDGETS","CRIPPLE","CRIPPLES","SPASTIC","IDIOT","IDIOTS","MORON",
            "MORONS","DUMB","STUPID","URANUS","DAMNIT","GODDAMN","JESUS","CHRIST","SATAN","HITLER","GUN","GUNS","BOMB","BOMBS"
        };

        static HashSet<string> set;

        public static bool IsBlocked(string word)
        {
            if (set == null) set = new HashSet<string>(List);
            return set.Contains(word.ToUpperInvariant());
        }
    }
}
