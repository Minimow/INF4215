etudiant(julien).

cours(inf1040).
cours(inf1010).
cours(inf1995).

requis(inf1995, [inf1040, inf1010]).

reussi(inf1010, julien).
reussi(inf1040, julien).

verifierPrerequis(Etudiant, []) :-
	etudiant(Etudiant).

verifierPrerequis(Etudiant, [Cours | Reste]) :-
	reussi(Cours, Etudiant),
	verifierPrerequis(Etudiant, Reste).

elligible(Cours, Etudiant) :-
	cours(Cours),
	etudiant(Etudiant),
	requis(Cours, Requis),
	verifierPrerequis(Etudiant, Requis).

elligible(Cours, Etudiant) :-
	cours(Cours),
	etudiant(Etudiant),
	\+ requis(Cours, _).
