# Kořenář
- Popsat podmíněné pravděpodobnosti
* N := matrix.len()
- Vektor absolutních pravděpodobností:
    - Značeno jako **p(n)**
    - Vektor pravděpodobností že stav je $p_i$ kde $i \in \{1, 2, ..., N}\$
- Matice pradvděpodobností přechodu
    - Značeno __P(n)__
    - $\[p_{ij}\]$ pro $i, j \in {1, 2, ..., N}$
    - $p_{ij}$ >= 0
    - $\sum \limits_{j=1}^{n} p_{ij} = 1$
    > if $(\forall a, b \in {1, 2, ...}) p_{ij}(a) == p_{ij}(b)$ { řetezec = homogenní } else { řetezec = nehomogenní }
- Pravděpodobnost stavu j v momentu t
    - $p_a(1) = p_a(0) * p_aa + p_b(0) * p_ba + ... = \sum \limits_{\alpha \in \{a, b, ...\}} p_{\alpha}(0) * p_{\alpha a}$
    - Maticově: **p(1)** = **p(0)** * **P**
        - **p(2)** = **p(1)** * **P** = **p(0)** * **P**^2
        - **p(n)** = **p(0)** * **P**^n
> if $p_{ii} > 0$ { stav = rekurentní } else { stav = tranzientní}
- Pokud je stav rekurentní, a je dosažitelný kdykoli, je ergodický, pokud po spočetném počtu kroků, potom je periodický, pokud po nekonečném počtu kroků, potom je stav rekurentní nulový

- $p^n_{ij} > 0$ -> stav je dosažitelný
    - Jinak nedosažitelný
    - Vzájemně dosažitelné stavy jsou sousledné
        - Skupina vzájemně dosžitelných stavů je uzavřená třída
        - Jenom jedna třída -> nerozložitelný (ireducibulní) řetezec
- Všechny stav jsou uzavřená třída a jsou ergodické -> řetezec je regulérní
- $(\exists n \in N) p^n_{ij} = 1$ => pohlcující (absorpční stav)
    - Ostatní stav jsou tranzientní (pravděpodobnost výskytu se blíží nule)
    - Absorpční řetězec

- Něco s rozložietlností matice, viz strana 14
- 
