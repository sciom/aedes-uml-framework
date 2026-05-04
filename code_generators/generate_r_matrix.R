#!/usr/bin/env Rscript
# ==============================================================================
# Skeleton Code Generator: R Stage-Structured Matrix Model
# ==============================================================================
#
# This script writes a skeleton R implementation of a stage- and age-structured
# matrix population model for Aedes mosquito population dynamics, based on the
# UML class diagram specification.
#
# The generated code provides:
#   - Stage-specific vital rate functions (development, survival, fecundity)
#   - Temperature- and photoperiod-dependent parameter modifiers
#   - Leslie/Lefkovitch matrix construction
#   - Time-step simulation loop
#   - Placeholder implementations marked with TODO
#
# Corresponds to the matrix population paradigm described in:
#   Lončarić & Hackenberger (2013) doi:10.1016/j.tpb.2012.08.002
#
# Usage:
#   Rscript generate_r_matrix.R > aedes_matrix_model.R
#
# Author: Aedes UML Framework
# License: MIT
# Repository: https://github.com/sciom/aedes-uml-framework
# ==============================================================================

cat('#!/usr/bin/env Rscript
# ==============================================================================
# Aedes Population Stage-Structured Matrix Model
# ==============================================================================
#
# Auto-generated skeleton from UML specification.
# Fill in the vital-rate implementations marked with TODO.
#
# Based on: UML-Based Framework for Aedes Population Dynamics
# Repository: https://github.com/sciom/aedes-uml-framework
# ==============================================================================

# ------------------------------------------------------------------------------
# Dependencies
# ------------------------------------------------------------------------------
# install.packages(c("Matrix", "deSolve"))  # uncomment if needed
library(Matrix)

# ==============================================================================
# 1. PARAMETERS
# ==============================================================================

#\' Default model parameters
#\'
#\' A named list of baseline vital rates and model settings. All rates are
#\' per-day unless otherwise noted.  Replace placeholder values with
#\' species-specific estimates.
default_params <- list(
  # Thermal thresholds (degC)
  T_min        = 10.0,   # TODO: species-specific lower threshold
  T_max        = 35.0,   # TODO: species-specific upper threshold
  T_opt        = 25.0,   # TODO: optimal temperature

  # Photoperiod threshold for diapause (hours)
  L_diapause   = 12.0,   # TODO: critical photoperiod

  # Baseline development rates (1/day at T_opt)
  d_E          = 0.10,   # Egg
  d_L          = 0.07,   # Larva (aggregate stage)
  d_P          = 0.15,   # Pupa

  # Baseline survival (daily probability at T_opt, no density dependence)
  s_E          = 0.95,   # Egg
  s_L          = 0.90,   # Larva
  s_P          = 0.92,   # Pupa
  s_Am         = 0.88,   # Adult male
  s_Af         = 0.88,   # Adult female

  # Fecundity
  fecundity    = 80.0,   # Eggs per female per gonotrophic cycle
  gonotrophic  = 4.0,    # Gonotrophic cycle length (days) at T_opt
  sex_ratio    = 0.5,    # Proportion female at emergence

  # Density dependence
  K            = 1000.0, # Larval carrying capacity (per breeding site)
  dd_alpha     = 1.0,    # Density-dependence shape parameter

  # Simulation
  latitude     = 45.0,   # Degrees north (for photoperiod)
  dt           = 1.0     # Time step (days)
)

# ==============================================================================
# 2. ENVIRONMENTAL DRIVER FUNCTIONS
# ==============================================================================

#\' Daily mean temperature (seasonal sinusoid placeholder)
#\'
#\' @param doy  Integer day of year (1-365)
#\' @param lat  Latitude (degrees north), used for amplitude scaling
#\' @return     Mean temperature (degC)
#\'
#\' TODO: Replace with observed time series or climate model output.
temperature <- function(doy, lat = 45.0) {
  # Simple sinusoidal approximation
  T_mean <- 15 + 10 * sin(2 * pi * (doy - 91) / 365)
  return(T_mean)
}

#\' Photoperiod (day length in hours)
#\'
#\' @param doy  Integer day of year (1-365)
#\' @param lat  Latitude (degrees north)
#\' @return     Photoperiod (hours)
photoperiod <- function(doy, lat = 45.0) {
  lat_rad   <- lat * pi / 180
  decl      <- 23.45 * sin(2 * pi * (284 + doy) / 365) * pi / 180
  cos_ha    <- -tan(lat_rad) * tan(decl)
  cos_ha    <- max(-1, min(1, cos_ha))
  hour_angle <- acos(cos_ha)
  return(2 * hour_angle * 180 / pi / 15)
}

#\' Daily precipitation (stochastic placeholder)
#\'
#\' @param doy  Integer day of year (1-365)
#\' @return     Precipitation (mm)
#\'
#\' TODO: Replace with observed series or stochastic weather generator.
precipitation <- function(doy) {
  # Placeholder: random draw from gamma distribution
  # TODO: parameterise with site-specific data
  return(max(0, rnorm(1, mean = 2, sd = 3)))
}

# ==============================================================================
# 3. TEMPERATURE-RESPONSE FUNCTIONS
# ==============================================================================

#\' Briere development rate function
#\'
#\' @param temp   Temperature (degC)
#\' @param T_min  Lower threshold (degC)
#\' @param T_max  Upper threshold (degC)
#\' @param a      Empirical coefficient
#\' @return       Development rate (1/day), 0 outside thermal window
#\'
#\' TODO: Fit a, T_min, T_max from laboratory data.
briere_rate <- function(temp, T_min = 10, T_max = 35, a = 1e-4) {
  if (temp <= T_min || temp >= T_max) return(0.0)
  return(a * temp * (temp - T_min) * sqrt(T_max - temp))
}

#\' Quadratic survival modifier
#\'
#\' @param temp   Temperature (degC)
#\' @param p      Parameter list (uses T_min, T_max, T_opt)
#\' @return       Survival modifier in [0, 1]
survival_modifier <- function(temp, p) {
  if (temp <= p$T_min || temp >= p$T_max) return(0.0)
  # Normalised quadratic peak at T_opt
  mod <- (temp - p$T_min) * (p$T_max - temp) /
         ((p$T_opt - p$T_min) * (p$T_max - p$T_opt))
  return(max(0, mod))
}

#\' Gonotrophic cycle length as function of temperature (days)
#\'
#\' @param temp   Temperature (degC)
#\' @param p      Parameter list
#\' @return       Gonotrophic cycle length (days)
#\'
#\' TODO: Replace linear approximation with empirical relationship.
gonotrophic_length <- function(temp, p) {
  if (temp <= p$T_min) return(Inf)
  # Simple linear approximation; replace with published function
  return(max(1, p$gonotrophic * p$T_opt / temp))
}

# ==============================================================================
# 4. DENSITY-DEPENDENCE
# ==============================================================================

#\' Larval density-dependent survival modifier
#\'
#\' @param L_total  Total larval abundance across instars
#\' @param p        Parameter list (uses K, dd_alpha)
#\' @return         Multiplicative survival reduction in (0, 1]
density_survival <- function(L_total, p) {
  return(1 / (1 + p$dd_alpha * L_total / p$K))
}

# ==============================================================================
# 5. MATRIX CONSTRUCTION
# ==============================================================================

#\' Build the stage-structured projection matrix for one time step
#\'
#\' Stages (columns/rows):
#\'   1 = Egg (E)
#\'   2 = Larva (L)   [aggregate; extend to age-classes if needed]
#\'   3 = Pupa (P)
#\'   4 = Adult male (Am)
#\'   5 = Adult female (Af)
#\'
#\' @param temp     Daily mean temperature (degC)
#\' @param L_total  Total larval abundance (for density dependence)
#\' @param p        Parameter list
#\' @param diapause Logical; if TRUE suppress egg hatching
#\' @return         5x5 projection matrix (Lefkovitch)
#\'
#\' TODO: Extend to age-within-stage structure (age classes per stage)
#\'       following the Lončarić & Hackenberger (2013) formulation.
build_matrix <- function(temp, L_total = 0, p = default_params,
                         diapause = FALSE) {

  # --- Vital rates at current temperature ---
  d_E <- briere_rate(temp, p$T_min, p$T_max) * p$d_E /
         briere_rate(p$T_opt, p$T_min, p$T_max)  # normalised development
  d_L <- briere_rate(temp, p$T_min, p$T_max) * p$d_L /
         briere_rate(p$T_opt, p$T_min, p$T_max)
  d_P <- briere_rate(temp, p$T_min, p$T_max) * p$d_P /
         briere_rate(p$T_opt, p$T_min, p$T_max)

  surv_mod <- survival_modifier(temp, p)
  dd_mod   <- density_survival(L_total, p)

  s_E  <- p$s_E  * surv_mod
  s_L  <- p$s_L  * surv_mod * dd_mod
  s_P  <- p$s_P  * surv_mod
  s_Am <- p$s_Am * surv_mod
  s_Af <- p$s_Af * surv_mod

  # Fecundity: eggs laid per female per day
  gono <- gonotrophic_length(temp, p)
  F_Af <- if (is.finite(gono)) p$fecundity / gono else 0.0

  # Diapause blocks egg development
  if (diapause) d_E <- 0.0

  # --- Lefkovitch matrix ---
  # A[i,j] = contribution of stage j to stage i in next step
  A <- matrix(0, nrow = 5, ncol = 5,
              dimnames = list(c("E","L","P","Am","Af"),
                              c("E","L","P","Am","Af")))

  # Egg: stay (undeveloped) or advance to larva; receive fecundity from Af
  A["E", "E"]  <- s_E  * (1 - d_E)   # stasis
  A["L", "E"]  <- s_E  * d_E          # advance to larva
  A["E", "Af"] <- F_Af                 # fecundity

  # Larva: stay or advance to pupa
  A["L", "L"]  <- s_L  * (1 - d_L)
  A["P", "L"]  <- s_L  * d_L

  # Pupa: stay or emerge as adult
  A["P", "P"]  <- s_P  * (1 - d_P)
  A["Am","P"]  <- s_P  * d_P * (1 - p$sex_ratio)
  A["Af","P"]  <- s_P  * d_P * p$sex_ratio

  # Adults: survival only (no development transition)
  A["Am","Am"] <- s_Am
  A["Af","Af"] <- s_Af

  return(A)
}

# ==============================================================================
# 6. SIMULATION
# ==============================================================================

#\' Run daily time-step simulation
#\'
#\' @param n0       Named numeric vector of initial abundances
#\'                 (names: E, L, P, Am, Af)
#\' @param n_days   Number of simulation days
#\' @param p        Parameter list
#\' @param doy_start  Starting day of year (default 1 = 1 Jan)
#\' @return         Matrix of abundances (rows = days, cols = stages)
simulate_aedes <- function(n0, n_days = 365, p = default_params,
                           doy_start = 1) {

  stages  <- c("E", "L", "P", "Am", "Af")
  results <- matrix(NA_real_, nrow = n_days + 1, ncol = length(stages),
                    dimnames = list(NULL, stages))
  results[1, ] <- n0[stages]

  n <- n0[stages]

  for (t in seq_len(n_days)) {
    doy  <- ((doy_start + t - 2) %% 365) + 1
    temp <- temperature(doy, p$latitude)
    phot <- photoperiod(doy, p$latitude)

    # Diapause check
    diap <- phot < p$L_diapause & temp < (p$T_min + 2)  # TODO: refine logic

    A <- build_matrix(temp, L_total = n["L"], p = p, diapause = diap)
    n <- as.vector(A %*% n)
    n <- pmax(n, 0)  # prevent negative abundances

    results[t + 1, ] <- n
  }

  day_index <- 0:n_days
  return(data.frame(day = day_index, results))
}

# ==============================================================================
# 7. ANALYSIS HELPERS
# ==============================================================================

#\' Compute dominant eigenvalue (asymptotic growth rate lambda) of matrix
#\'
#\' @param A  Projection matrix
#\' @return   Dominant eigenvalue (lambda_1)
lambda1 <- function(A) {
  ev <- eigen(A, only.values = TRUE)$values
  return(max(Re(ev)))
}

#\' Stable stage distribution from projection matrix
#\'
#\' @param A  Projection matrix
#\' @return   Numeric vector (proportional stable stage distribution)
stable_stage <- function(A) {
  ev  <- eigen(A)
  idx <- which.max(Re(ev$values))
  w   <- Re(ev$vectors[, idx])
  return(w / sum(w))
}

#\' Sensitivity matrix (partial derivative of lambda w.r.t. each element)
#\'
#\' @param A  Projection matrix
#\' @return   Matrix of sensitivities
sensitivity <- function(A) {
  ev  <- eigen(A)
  idx <- which.max(Re(ev$values))
  w   <- Re(ev$vectors[, idx])               # right eigenvector
  v   <- Re(solve(t(ev$vectors))[idx, ])     # left eigenvector
  return(outer(v, w) / as.numeric(v %*% w))
}

#\' Elasticity matrix
#\'
#\' @param A  Projection matrix
#\' @return   Matrix of elasticities
elasticity <- function(A) {
  lam <- lambda1(A)
  S   <- sensitivity(A)
  return(A * S / lam)
}

# ==============================================================================
# 8. EXAMPLE USAGE
# ==============================================================================

if (!interactive()) {
  cat("Running Aedes matrix model skeleton...\\n")

  p <- default_params

  # Initial population: 1000 eggs, 10 adult females
  n0 <- c(E = 1000, L = 0, P = 0, Am = 0, Af = 10)

  # Simulate one year starting on day 1 (1 Jan)
  res <- simulate_aedes(n0, n_days = 365, p = p, doy_start = 1)

  cat(sprintf("Final abundances after 365 days:\\n"))
  cat(sprintf("  Eggs:   %.0f\\n", tail(res$E,  1)))
  cat(sprintf("  Larvae: %.0f\\n", tail(res$L,  1)))
  cat(sprintf("  Pupae:  %.0f\\n", tail(res$P,  1)))
  cat(sprintf("  Adults (M+F): %.0f\\n", tail(res$Am + res$Af, 1)))

  # Example: dominant eigenvalue at reference temperature
  A_ref <- build_matrix(temp = p$T_opt, p = p)
  cat(sprintf("\\nDominant eigenvalue (lambda) at T_opt = %.1f°C: %.4f\\n",
              p$T_opt, lambda1(A_ref)))
  cat(sprintf("Stable stage distribution at T_opt:\\n"))
  ssd <- stable_stage(A_ref)
  cat(sprintf("  E=%.3f  L=%.3f  P=%.3f  Am=%.3f  Af=%.3f\\n",
              ssd[1], ssd[2], ssd[3], ssd[4], ssd[5]))
}
')
