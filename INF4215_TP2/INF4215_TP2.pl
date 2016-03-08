etudiant(julien).

cours(log1000).
cours(log2000).
cours(log3000).

requis(log2000, log1000).
requis(log3000, log2000).

reussi(log1000, julien).

elligible(Cours, Etudiant) :-
	cours(Cours),
	etudiant(Etudiant),
	requis(Cours, Requis),
	reussi(Requis, Etudiant).

elligible(Cours, Etudiant) :-
	cours(Cours),
	etudiant(Etudiant),
	\+ requis(Cours, _).
