etudiant(julien).

cours(log1000).
cours(log2000).
cours(log3000).

requis(log3000, log2000).
reussi(log1000, julien).

elligible(cours, etudiant) :-
	cours(cours),
	etudiant(etudiant),
	requis(cours, requis),
	reussi(requis, etudiant).

elligible(cours, etudiant) :-
	cours(cours),
	etudiant(etudiant),
	true \= requis(cours, requis).

