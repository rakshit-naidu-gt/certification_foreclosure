# Referee check of the proofs in "certification foreclosure" (files/model.tex, regulator.tex, appendix.tex)

## 0. Setting (restated so this report stands alone)

State $q_t\in\mathbb R$, investment $c_t\ge 0$, dynamics $q_{t+1}=q_t+f(c_t)-\delta$, $\delta>0$.
Assumption 1: $f:\mathbb R_+\to\mathbb R_+$ strictly increasing, strictly concave, $f(0)=0$, $f'(0^+)=\infty$, $f'(\infty)=0$.
Assumption 2: $L$ strictly decreasing, strictly convex, $L\ge 0$. Assumption 3: $p_L=\rho p_H$, $\rho\in(0,1)$.
Both $f,L$ are taken $C^2$ (the paper says so inside the proof of Prop. 1).
The myopic firm at state $q$ facing scrutiny $p$ minimises $J(c;q,p)=c+\beta pL(q+f(c)-\delta)$; the FOC is
$\beta p\,|L'(q')|\,f'(c)=1$, $q'=q+f(c)-\delta$. Its solution is $c^*(q,p)$, and $h_p(q)=q+f(c^*(q,p))-\delta$.
Assumption 4: $c_\delta=f^{-1}(\delta)$ exists and for each $p>0$ there is a unique $q^*(p)$ with
$\beta p|L'(q^*(p))|f'(c_\delta)=1$.
Recurring rule: $p=p_H$ if $q_t<\tau$, $p=p_L$ if $q_t\ge\tau$. Noisy rule: $p(q)=p_H-\pi(q)(p_H-p_L)$.
Write $H(q)=h_{p_H}(q)$ for $q<\tau$ and $H(q)=h_{p_L}(q)$ for $q\ge\tau$.

Throughout, write **(S)** for the strengthening "$L''>0$ and $f''<0$ everywhere". Strict convexity and strict concavity alone give only $L''\ge0$ and $f''\le0$, which can vanish at isolated points.

## 1. Summary

| Result | Verdict |
|---|---|
| Prop. 1 (investment drop) | Correct, given (S) (or given $L'f''>0$ pointwise, which also needs a strict sign). |
| Lemma 1 (joint monotonicity) | Correct, given (S): $\partial c^*/\partial q<0$ needs $L''>0$. |
| Cor. 1 (slope bound $h_p'\in(0,1)$) | Correct, given (S). Algebra checked. |
| Cor. 2 (kink) | Correct. The paper says the condition can't be solved in closed form, but it is in fact equivalent to $q^*(p_L)<\tau\le q^*(p_H)$ (§3). |
| Prop. 2, Cor. 3 (comparative statics of $q^*$) | Correct. |
| Thm. 1 (recurring audits) (a) | Correct conclusion; the proof omits starts with $q_0<\tau$. Easy fix (§4). |
| Thm. 1 (c) | The statement "never certified from any $q_0$" is **false** when $q_0\ge\tau$: the firm is certified for finitely many periods. The step "never exceeds $q^*(p_H)$" is false when $q_0>q^*(p_H)$. The limit claim is correct (§4). |
| Thm. 1 (b) | **Not proved.** Nothing in the proof establishes convergence to a limit cycle (a periodic orbit). The argument for "time average strictly below $q^*(p_H)$" is a non-sequitur. A correct weaker statement with full proof is in §4. |
| Prop. 3 (forward-looking steady state) | Algebra correct, conditional on $V$ being differentiable and the steady state existing (the paper assumes the latter). Applying it to Case (a) is heuristic (§5). |
| Prop. 4, Remark, Cor. 4 (heterogeneity) | Correct up to small gaps: existence of $\rho_A$ needs continuity of $q^*$ (true; §6); the Remark ignores Case (c); $\bar q_B$ is not well defined. |
| Prop. 5 (imperfect observation) | The existence/uniqueness proof has a gap; it is repaired in §7, where the kink condition turns out to be unnecessary. The headline "no cycling for every $\sigma>0$" is **false for small $\sigma$** under the logistic $\pi$: the steady state becomes repelling (§7). The paper's numerical check uses a different model (§8). |
| Prop. 6 (flat regions) | Correct, with the Case (c) initial-condition caveat. |
| Appendix closed form; numbers | Correct (§9). |

## 2. Props 1, Lemma 1, Cor 1

**Existence of the interior optimum.** $J'(c)=1+\beta pL'(q+f(c)-\delta)f'(c)$.
- As $c\to0^+$: $L'(q+f(c)-\delta)\to L'(q-\delta)<0$, which is finite, and $f'\to\infty$, so $J'\to-\infty$.
- As $c\to\infty$: $|L'|$ is non-increasing (by convexity) and $q+f(c)-\delta\ge q-\delta$, so $|L'(\cdot)|\le|L'(q-\delta)|$, and $f'\to0$. Hence $J'\to1$.
- So a root exists.

**Uniqueness.** $J''=\beta p[L''f'^2+L'f'']$. This is $>0$ under (S), and it is $\ge0$ with possible zeros under the stated assumptions alone. The implicit-function signs are as the paper states: $J_{cp}=\beta L'f'<0$ and $J_{cq}=\beta pL''f'>0$.

**Cor. 1.** $h_p'=1+f'\,\partial c^*/\partial q=1-f'N/D$, where $N=\beta pL''f'$ and $D=J''$. Then $D-f'N=\beta pL'f''$, so $h_p'=L'f''/(L''f'^2+L'f'')\in(0,1)$ under (S). Verified.

**Remark on Section 2's text.** It says the myopic FOC "is exact if $p$ is constant forever and $V'\propto L'$". This conflicts with Prop. 3: there the factor is $V'=pL'/(1-\beta)$, so the myopic FOC (factor $1$) is not exact.

## 3. Fixed points of $h_p$, and the kink condition

**Lemma A.** $h_p(q)=q$ iff $q=q^*(p)$. Moreover, $\operatorname{sign}(h_p(q)-q)=\operatorname{sign}(p-P(q))$, where $P(q):=1/(\beta f'(c_\delta)|L'(q)|)$. $P$ is continuous and strictly increasing, with $P(q^*(p))=p$.

*Proof.*
1. $h_p(q)>q$ iff $c^*>c_\delta$.
2. Since $J'$ is strictly increasing in $c$, $c^*>c_\delta$ iff $J'(c_\delta)<0$.
3. At $c=c_\delta$ we have $q'=q$, so $J'(c_\delta)<0$ iff $\beta p|L'(q)|f'(c_\delta)>1$, i.e. iff $p>P(q)$.
4. Equality throughout gives the fixed-point statement. ∎

**Consequences.**
- $q\mapsto f(c^*(q,p))-\delta$ is strictly decreasing (Lemma 1) and vanishes exactly at $q^*(p)$.
- So the kink condition $f(c^*(\tau,p_L))<\delta\le f(c^*(\tau,p_H))$ holds **iff** $q^*(p_L)<\tau\le q^*(p_H)$. It is solvable in closed form.
- $q^*(p)=P^{-1}(p)$ is continuous, as the inverse of a continuous strictly monotone function.

The Cor. 2 proof is otherwise correct. Before certification ($q<\tau$): $f(c^*(q,p_H))>f(c^*(\tau,p_H))\ge\delta$. After certification ($q\ge\tau$): $f(c^*(q,p_L))\le f(c^*(\tau,p_L))<\delta$. Under the permanent rule (eq. pt) the decline in fact continues for ever, monotonically toward $q^*(p_L)$.

**Monotone convergence (used below).** Under (S), $h_p$ is increasing with $h_p(q^*)=q^*$, and $h_p(q)>q$ for $q<q^*$.
- So for $q<q^*$: $q<h_p(q)<q^*$. The orbit increases, is bounded, and converges to a fixed point, which can only be $q^*$.
- The case $q>q^*$ is symmetric.
- This uses the *global* fact $h_p'>0$. The paper phrases it via $|h_p'(q^*)|<1$, a local condition that would not suffice on its own; Cor. 1 supplies the global fact.

Props 2 and Cor. 3 follow from $q^*(p)=P^{-1}(p)$: $P$ increases in $q$, and $f'(c_\delta)$ decreases in $\delta$. Correct as written.

## 4. Theorem 1, corrected statements with proofs

Write $h_H=h_{p_H}$, $h_L=h_{p_L}$, $q_H=q^*(p_H)$, $q_L=q^*(p_L)$. Then $q_L<q_H$ by Prop. 2, since $\rho<1$.

**(a) $\tau\le q_L$.**
1. If $q_0<\tau$, the orbit follows $h_H$ and increases toward $q_H>\tau$, so it reaches $[\tau,\infty)$ in finite time.
2. On $[\tau,\infty)$ the orbit follows $h_L$:
   - from $q\ge q_L$, $h_L(q)\in[q_L,q]$;
   - from $\tau\le q<q_L$, $h_L(q)\in(q,q_L)$.
3. Either way the next state is $\ge\tau$. So the firm stays certified, and $q_t\to q_L$. ∎
(The paper's proof covers only step 2.)

**(c) $\tau\ge q_H$.**
- If $q_0<\tau$: by induction $q_t<\tau$ for all $t$. Indeed, if $q_t<\tau$ then $q_{t+1}=h_H(q_t)$. When $q_t\le q_H$ this lies in $[q_t,q_H]$, which is $<\tau$ unless $q_t=q_H=\tau$, impossible since $q_t<\tau$. When $q_H<q_t<\tau$ it lies in $(q_H,q_t)$. So the firm is never certified, and $q_t\to q_H$.
- If $q_0\ge\tau$: the firm **is** certified. Under $h_L$ the orbit decreases toward $q_L<\tau$, so certification lasts only finitely many periods; after that the case above applies.
- Corrected statement: *the firm is certified at most finitely often, never if $q_0<\tau$, and $q_t\to q_H$.*
- The paper's "never exceeds $q_H$" also fails for $q_0>q_H$.

**(b) $q_L<\tau<q_H$.** What can be proved:

*(i) Infinitely many crossings.* From $q\ge\tau$, the orbit follows $h_L$ and decreases toward $q_L<\tau$, so it falls below $\tau$ in finite time. From $q<\tau$, it follows $h_H$ and increases toward $q_H>\tau$, so it reaches $\ge\tau$ in finite time. Hence the firm alternates between certified and exposed for ever.

*(ii) Trapping interval.* Let $I=[h_L(\tau),h_H(\tau))$. Then $q_L<h_L(\tau)<\tau<h_H(\tau)<q_H$ (by Lemma A and monotonicity of $h_p$).
- *Upper bound.* Suppose $q_t<h_H(\tau)$. If $q_t<\tau$, then $q_{t+1}=h_H(q_t)<h_H(\tau)$. If $q_t\ge\tau$, then $q_{t+1}=h_L(q_t)<q_t$.
- *Lower bound.* Suppose $q_t\ge h_L(\tau)$. If $q_t\ge\tau$, then $q_{t+1}=h_L(q_t)\ge h_L(\tau)$. If $q_t<\tau$, then $q_{t+1}>q_t$.
- Each bound is invariant once it holds. Each is attained after the first crossing in the appropriate direction, and by (i) such crossings occur.
- So $q_t\in I$ for all large $t$.

*(iii) Long-run averages.* From (ii),
$$\limsup_T \frac1T\sum_{t<T}q_t\le h_H(\tau)<q_H,\qquad \liminf_T\frac1T\sum_{t<T}q_t\ge h_L(\tau)>q_L.$$
This proves the theorem's welfare comparison for Case (b), with the time average read as a limsup.

The paper argues instead that "the orbit never reaches its supremum $q_H$, so its average is strictly below $q_H$". That does not follow: a sequence can stay below its supremum while its average tends to that supremum. The bound in (iii) is what makes the comparison valid.

Calibration check: $h_L(0.8)=0.8+0.0275-0.045=0.7825$ and $h_H(0.8)=0.8+0.0858-0.045=0.8408$. These match the simulated tail range $[0.783,0.840]$.

*(iv) What is not proved: "converges to a limit cycle".*
- On $I$, $H$ is a piecewise increasing contraction (slopes in $(0,1)$) with a single discontinuity at $\tau$. This is the class of maps that includes contracted rotations, $x\mapsto\lambda x+\mu \bmod 1$.
- In that class, some parameter values give an irrational rotation number. Those maps have no periodic orbit; the attractor is a Cantor set and the orbits are quasi-periodic.
- The proof contains no argument that excludes this, so a periodic limit cycle is not established.
- The simulation reports an oscillation "with a period of 3–4 audit cycles". That fits a long-period or quasi-periodic orbit as well as a short cycle.
- What would repair the claim: either prove a periodic orbit exists for the parameters in question, or weaken the statement to (i)–(iii). Typical-parameter periodicity is the usual result for such families, but it would need its own proof here.

**Final sentence of Thm. 1.** It holds in the forms (a), (iii) and (c) above.

## 5. Prop. 3 (forward-looking)

Bellman equation: $V(q)=pL(q)+\min_c[c+\beta V(q+f(c)-\delta)]$. The envelope step gives $V'(q)=pL'(q)+\beta V'(q')$. At a steady state with $c=c_\delta$ this yields $V'=pL'/(1-\beta)$. The FOC then gives $\beta\frac{p}{1-\beta}|L'|f'(c_\delta)=1$, so $q^\dagger(p)=q^*(p/(1-\beta))>q^*(p)$. **Correct**, given:
- $V$ is differentiable at $q^\dagger$ (needed for the envelope step, and not stated);
- the steady state exists (stated as a hypothesis).

Caveat on the claimed scope. Under the state-contingent rule, a forward-looking firm in Case (a) does not face "$p$ constant forever": its off-path deviations below $\tau$ change $p$. The proposition applies only if the constant-$p_L$ optimal policy keeps the state $\ge\tau$ near $q^\dagger$, which is not shown. Also, the case boundaries for the forward-looking firm should be stated in terms of $q^\dagger$, not $q^*$.

## 6. Heterogeneity

**Prop. 4.** $\rho\mapsto q^*(\rho p_H)$ is continuous and strictly increasing (§3). With $\lim_{\rho\to0}q^*(\rho p_H)<\tau<q_H$, the intermediate value theorem gives a unique $\rho_A\in(0,1)$. The sorting then follows from Thm. 1's case conditions. **Correct.** Calibration: $q^*(p)\to-1<0.8$ as $p\to0$.

**Remark.** When $p_{H,i}$ varies, a firm with $\tau\ge q^*(p_{H,i})$ is in Case (c), not Case (b). So "Case (b) otherwise" needs that extra condition. Also, $\delta_i$ does not enter $p_{L,i}$; the sorting variable is $q^*(p_{L,i},\delta_i)$.

**Cor. 4.** The integrand satisfies $<q_H$ pointwise (by §4(iii) and Prop. 2), so the loss is strictly positive. But $\bar q_B$ must be defined, e.g. as the limsup average (which may depend on $q_0$), and the integrand must be measurable.

## 7. Prop. 5 (imperfect observation)

Let $g(q)=f(c^*(q,p(q)))-\delta$ and $k(q)=q+g(q)$.

**Monotonicity.** "$g$ strictly decreasing" is correct, given (S) and $\pi$ increasing.

**Gap in the existence proof.** The proof bounds $f(c^*(q,p_H))$ and then passes to $p(q)$ as $q\to-\infty$ "by joint continuity". Continuity on an unbounded domain gives no uniformity, so this step is unjustified.

**Repair.** Since $p_L<p(q)<p_H$ and $c^*$ is increasing in $p$,
$$f(c^*(q,p_L))-\delta<g(q)<f(c^*(q,p_H))-\delta .$$
By §3, this gives $g>0$ on $(-\infty,q_L]$ and $g<0$ on $[q_H,\infty)$. So the unique root satisfies $q^{**}\in(q_L,q_H)$. **The kink condition is not needed for existence or uniqueness.** By Lemma A, $q^{**}$ is characterised by $p(q^{**})=P(q^{**})$.

**$q^{**}(\sigma)\to\tau$.** Assume $q_L<\tau<q_H$ (the kink condition), so $p_L<P(\tau)<p_H$. Fix a small $\varepsilon>0$.
- As $\sigma\to0$: $p(\tau-\varepsilon)\to p_H>P(\tau-\varepsilon)$, and $p(\tau+\varepsilon)\to p_L<P(\tau+\varepsilon)$.
- By Lemma A, for small $\sigma$ this gives $g(\tau-\varepsilon)>0>g(\tau+\varepsilon)$, so $q^{**}\in(\tau-\varepsilon,\tau+\varepsilon)$. **Correct.**

**Claim refuted: "no cycling for any $\sigma>0$".** The paper's own proviso ("no single-period overshoot") fails for small $\sigma$. Take the logistic $\pi$, with $\pi'=\pi(1-\pi)/\sigma$. By the chain rule,
$$k'(q^{**})=h'_{p^{**}}(q^{**})-A\,(p_H-p_L)\,\frac{\theta_\sigma(1-\theta_\sigma)}{\sigma},$$
where:
- $\theta_\sigma=\pi(q^{**})=(p_H-P(q^{**}))/(p_H-p_L)$;
- $A=f'\,\partial c^*/\partial p=|L'|f'^2/\big(p[L''f'^2+L'f'']\big)>0$, evaluated at $c=c_\delta$, $q'=q^{**}$, $p=p^{**}$;
- $h'\in(0,1)$.

As $\sigma\to0$:
- $q^{**}\to\tau$, so $\theta_\sigma\to\theta_0=(p_H-P(\tau))/(p_H-p_L)\in(0,1)$;
- $A\to A_0>0$ by continuity;
- hence $k'(q^{**})\to-\infty$.

So there is a $\sigma_0>0$ such that $|k'(q^{**})|>1$ for all $\sigma<\sigma_0$, and the fixed point is repelling. Consequences:
- **Only orbits that land exactly on $q^{**}$ converge.** By continuity of $k'$ there is a neighbourhood $U$ and a $\lambda>1$ with $|k(q)-q^{**}|\ge\lambda|q-q^{**}|$ on $U$. A convergent orbit eventually stays in $U$, where its distance to $q^{**}$ grows geometrically unless it is zero.
- **Every other orbit oscillates across $q^{**}$ for ever.** If such an orbit were eventually on one side of $q^{**}$, it would be eventually monotone (by the sign of $g$) and bounded. It would then converge to a fixed point, which must be $q^{**}$, a contradiction. So it crosses $q^{**}\approx\tau$ infinitely often: cycling persists.

**Calibrated numbers** ($q=\tau=0.8$, $c_\delta=0.0225$, $P(\tau)=0.50155$):

| Quantity | Value |
|---|---|
| $\lvert L'\rvert$ | $2.0988$ |
| $L''$ | $2.3320$ |
| $f'$ | $1$ |
| $f''$ | $-22.222$ |
| $h'$ | $0.9524$ |
| $A_0$ | $0.08545$ |
| $\theta_0$ | $0.7121$ |
| $k'(q^{**})$ | $\approx 0.952-0.01226/\sigma$ |

So the fixed point is repelling for $\sigma\lesssim0.0063$ (leading-order estimate). The paper reports convergence down to $\sigma=0.0002$; that is explained in §8.

## 8. Numerical claims vs. the proven model

`recurring_sim/imperfect_obs.py` does not simulate Prop. 5's model. It evaluates scrutiny at the *next* state, $p(q_{t+1})$, and it adds a term $|p'(q_{t+1})|L(q_{t+1})$ to the FOC. In Prop. 5 the scrutiny is evaluated at the current state $q$ and the FOC is the paper's own one-period FOC. In the simulated model:
- Lemma 1 and the proof of Prop. 5 do not apply;
- $J$ need not be convex, since $p(q')L(q')$ need not be convex in $c$, and the root-finder returns some root of the FOC.

So §sim-imperfectobs neither verifies Prop. 5 nor contradicts §7.

`recurring_audit_sim.py` uses current-state $p$, which is consistent with Thm. 1.

## 9. Minor items checked

**Appendix closed form.**
- $(q^*+1)^2=\beta pa^2b/(2\delta)$ is correct. With the calibration, $(q^*+1)^2=6.46p$.
- $q^*(1)=1.5417$, $q^*(0.3)=0.3921$, $q^*(0.6)=0.9688$, and $\rho_A=3.24/6.46=0.50155$. All match the paper.
- At $\tau$: $c^*(\tau,p_H)=0.0818$ and $c^*(\tau,p_L)=0.0084$ satisfy the FOC to rounding.

**Slope values quoted in Thm. 1's proof.**
- For $f=a\sqrt c$, $L=b/(q+1)$: $h'(q^*)=(q^*+1)/(q^*+1+2\delta)$, giving $0.966$ and $0.939$. ✓
- For $f=ac^{1/3}$, $L=be^{-q}$: $h'=1/(1+\delta/2)=0.978$, independent of $p$. ✓
- Alternative-form steady states: $q^*(p_H)=\ln 83.26=4.422$ and $q^*(p_L)=3.218$. ✓

**Prop. 6.** Correct; the Case (c) caveat from §4 applies.

**Regulator text.** It says a $\tau$ in Case (c) "induces zero investment forever". In fact the firm invests $c_\delta>0$ forever at $q_H$.

## 10. What remains open

- Whether Thm. 1(b)'s orbit actually converges to a periodic cycle for the calibrated parameters, or for generic parameters. This needs a rotation-number argument for the specific map $H$ on $I$.
- The exact threshold $\sigma_0$ below which Prop. 5's steady state is repelling. Only a leading-order estimate ($\approx0.0063$ at the calibration) is given here.
- Existence and differentiability of $V$ in Prop. 3. The paper also leaves this open.
