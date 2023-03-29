program cntlatm_check
    ! Check the AERA FCG namelist against the standard one
    implicit none

    ! Maximum length of scenarios
    integer, parameter :: lenscen=1000
    ! Number of well-mixed greenhouse gases
    Integer, Parameter :: NWMGHG   = 9

    ! Number of sulphate loading patterns
    Integer, Parameter :: NSULPAT  = 2

    ! Number of such scenarios, made up of:
    Integer, Parameter :: NCLMFCGS = NWMGHG + NSULPAT

    !  Indices indicating which scenario corresponds to which forcing:
    Integer, Parameter :: S_CO2     = 1
    Integer, Parameter :: S_CH4     = 2
    Integer, Parameter :: S_N2O     = 3
    Integer, Parameter :: S_CFC11   = 4
    Integer, Parameter :: S_CFC12   = 5
    Integer, Parameter :: S_SO4     = 6
    Integer, Parameter :: S_CFC113  = 8
    Integer, Parameter :: S_HCFC22  = 9
    Integer, Parameter :: S_HFC125  = 10
    Integer, Parameter :: S_HFC134A = 11

    logical :: l_clmchfcg
    ! Years at which a rate or level is specified
    Integer     :: CLIM_FCG_YEARS(LENSCEN,NCLMFCGS)
    Integer     :: CLIM_FCG_YEARS_AERA(LENSCEN,NCLMFCGS)

    ! Number of such years, for each forcing
    Integer     :: CLIM_FCG_NYEARS(NCLMFCGS), CLIM_FCG_NYEARS_AERA(NCLMFCGS)

    ! Values, or rates of increase, for the designated years.
    !  See GAS_CALC (in Section 70) or the umui panels for details.
    Real        :: CLIM_FCG_LEVLS(LENSCEN,NCLMFCGS)
    Real        :: CLIM_FCG_LEVLS_AERA(LENSCEN,NCLMFCGS)
    Real        :: CLIM_FCG_RATES(LENSCEN,NCLMFCGS)

    integer :: igas, i

    NAMELIST / CLMCHFCG /  CLIM_FCG_NYEARS, CLIM_FCG_YEARS,           &
                           CLIM_FCG_LEVLS,  CLIM_FCG_RATES,           &
                           L_CLMCHFCG

    ! open(unit=1, file='fcg_aera', status='old')
    open(unit=1, file='CNTLATM_ssp126_template_AERA', status='old')
    read(1,nml=clmchfcg)
    CLIM_FCG_NYEARS_AERA = CLIM_FCG_NYEARS
    CLIM_FCG_YEARS_AERA = CLIM_FCG_YEARS
    CLIM_FCG_LEVLS_AERA = CLIM_FCG_LEVLS
    close(1)
    open(unit=1, file='CNTLATM_ssp126_template_CMIP6', status='old')
    read(1,nml=clmchfcg)
    close(1)

    do igas=1,11
        if ( igas==6 .or. igas==7) cycle
        print*, igas, maxval(abs(CLIM_FCG_LEVLS_AERA(:86,1)-CLIM_FCG_LEVLS(:86,1)))
        print*, igas, maxval(abs(CLIM_FCG_LEVLS_AERA(87:486,1)-CLIM_FCG_LEVLS(86,1)))
        ! Check years
        print*, igas, maxval(abs(CLIM_FCG_YEARS_AERA(:486,igas)-(/ (i, i=2015,2500) /)))
    end do

end program cntlatm_check