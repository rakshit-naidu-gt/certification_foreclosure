# Notes — checking proofs in certification_foreclosure paper

Paper sources: files/model.tex (all formal results), files/regulator.tex (Prop flatregions), files/appendix.tex (closed form), files/simulation.tex (numbers).
Calibration: f=a√c, L=b/(q+1), a=.30, b=6.80, β=.95, δ=.045, τ=.80, p_H=1, ρ=.30.

## Verdicts (settled)
- Prop 1 (drop): correct. Existence: J'→-∞ as c→0+ (Inada, L'(q-δ)<0 finite), J'→1 as c→∞ (|L'(q+f-δ)|≤|L'(q-δ)|). Tech gap: strict convexity/concavity give only L''≥0, f''≤0; J''>0 needs L''>0 or f''<0 strictly pointwise. Fix: assume L''>0, f''<0.
- Lemma cstar: correct (∂c*/∂q<0 needs L''>0 strictly).
- Cor slopebound: algebra verified; h'=L'f''/(L''f'^2+L'f'')∈(0,1). Needs strict L''>0,f''<0.
- Kink cor: correct; moreover condition ⇔ q*(p_L)<τ≤q*(p_H) (closed form, contrary to text). Proof: f(c*(q,p))-δ strictly decr in q, zero at q*(p).
- Fixed points of h_p = q*(p): verified both directions.
- Prop steadystate, Cor delta: correct.
- Thm recurring:
  * (a) proof omits q0<τ start; fix: under p_H rises to q*(p_H)>q*(p_L)≥τ, crosses τ finitely. ok.
  * (c) "never certified from any q0" FALSE if q0≥τ (certified finitely many periods), and "never exceeds q*(p_H)" false for q0>q*(p_H). Limit claim right.
  * (b) "converges to limit cycle" NOT proved; map is piecewise-increasing contraction w/ one discontinuity (contracted-rotation type) — can have irrational rotation number / Cantor attractor, no periodic orbit. Proved: crosses τ infinitely often; eventually in [h_L(τ), h_H(τ)); limsup time avg ≤ h_H(τ) < q*(p_H). Paper's "never reaches sup ⇒ avg strictly below" is a non-sequitur; replace with this bound.
  * Numbers 0.966/0.939/0.978 verified: h'=(q*+1)/(q*+1+2δ) for baseline; 1/(1+δ/2) for alt.
- Prop forwardlooking: algebra correct given V differentiable & steady state exists. Caveat: state-contingent rule ≠ constant p (off-path), so application to Case (a) heuristic.
- Prop heterogeneous: correct; existence of ρ_A needs continuity of q* (true, inverse of continuous strictly monotone). Remark: ignores Case (c) when p_H,i varies; δ_i doesn't enter p_L,i.
- Cor aggwelfare: positivity ok using bound above; q̄_B needs definition (limsup/initial cond).
- Prop imperfectobs:
  * monotonicity of g ok.
  * limit argument q→-∞ uses joint continuity w/o uniformity: gap. Clean fix: p_L<p(q)<p_H ⇒ f(c*(q,p_L))-δ < g(q) < f(c*(q,p_H))-δ, so g>0 for q≤q*(p_L), g<0 for q≥q*(p_H); root in (q*(p_L),q*(p_H)) — kink condition unnecessary.
  * q**→τ: ok (cleaner via p(q**)=P(q**), P(q)=1/(βf'(c_δ)|L'(q)|)).
  * MAJOR: "no cycling for every σ>0" false for small σ: k'(q**) = h' - f'∂c*/∂p (p_H-p_L) π'(q**), π'(q**)=θ(1-θ)/σ, θ→(p_H-P(τ))/(p_H-p_L)∈(0,1) ⇒ k'(q**)→-∞. Calibration: h'≈.9524, coefficient ≈ .01226/σ ⇒ unstable for σ < ≈0.0063.
  * Sim (imperfect_obs.py) uses DIFFERENT model: p evaluated at q_{t+1} with extra |p'|L term in FOC. So numerical "verification" does not test the proposition's model.
- Prop flatregions: correct modulo (c) initial-condition caveat. Text "zero investment forever" wrong (c_δ>0).
- Appendix closed form: correct; numbers q*(p_H)=1.5417, q*(.3)=.3921, q*(.6)=.9688, ρ_A=.50155 verified; c* values at τ verified.

## Status
DONE: proof.md written. Nothing further to do.
