from .hvss_common import Metric, ImpactType, ImpactTypes, MetricGroup, MetricCode

# =====  EXP - Exploitability Metrics  ==========================================

# [AV] Attack Vector    [N,A,L,P]    [Network, Adjacent Network, Local, Physical]
metric_av_n = Metric(code='N', index=1, name='Network')
metric_av_a = Metric(code='A', index=2, name='Adjacent Network')
metric_av_l = Metric(code='L', index=3, name='Local')
metric_av_p = Metric(code='P', index=4, name='Physical')
metric_group_av = MetricGroup(code='AV', name='Attack Vector', metrics={
    metric_av_n.code: metric_av_n,
    metric_av_a.code: metric_av_a,
    metric_av_l.code: metric_av_l,
    metric_av_p.code: metric_av_p
})

# [EAC] Extended Attack Complexity    [N,L,M,H,C,E]    [Negligible, Low, Medium, High, Critical, Extreme]
metric_eac_n = Metric(code='N', index=1, name='Negligible')
metric_eac_l = Metric(code='L', index=2, name='Low')
metric_eac_m = Metric(code='M', index=3, name='Medium')
metric_eac_h = Metric(code='H', index=4, name='High')
metric_eac_c = Metric(code='C', index=5, name='Critical')
metric_eac_e = Metric(code='E', index=6, name='Extreme')
metric_group_eac = MetricGroup(code='EAC', name='Extended Attack Complexity', metrics={
    metric_eac_n.code: metric_eac_n,
    metric_eac_l.code: metric_eac_l,
    metric_eac_m.code: metric_eac_m,
    metric_eac_h.code: metric_eac_h,
    metric_eac_c.code: metric_eac_c,
    metric_eac_e.code: metric_eac_e
})

# [PR] Privileges Required    [N,L,H]    [None, Low, High]
metric_pr_n = Metric(code='N', index=1, name='None')
metric_pr_l = Metric(code='L', index=2, name='Low')
metric_pr_h = Metric(code='H', index=3, name='High')
metric_group_pr = MetricGroup(code='PR', name='Privileges Required', metrics={
    metric_pr_n.code: metric_pr_n,
    metric_pr_l.code: metric_pr_l,
    metric_pr_h.code: metric_pr_h
})

# [UI] User Interaction    [N,R]     [None, Required]
metric_ui_n = Metric(code='N', index=1, name='None')
metric_ui_r = Metric(code='R', index=2, name='Required')
metric_group_ui = MetricGroup(code='UI', name='User Interaction', metrics={
    metric_ui_n.code: metric_ui_n,
    metric_ui_r.code: metric_ui_r
})

metric_group_exp = MetricGroup(code='EXP', name='Exploitability',
                               description='The ease and technical means by which the vulnerability can be exploited',
                               metrics={
                                   metric_group_av.code: metric_group_av,
                                   metric_group_eac.code: metric_group_eac,
                                   metric_group_pr.code: metric_group_pr,
                                   metric_group_ui.code: metric_group_ui
                               })

# =====  XIT - eXtended Impact Type Metrics  ==========================================

xit_xcia_c_n = Metric(code='N', index=1, name='None')
xit_xcia_c_l = Metric(code='L', index=2, name='Low')
xit_xcia_c_h = Metric(code='H', index=3, name='High')
xit_xcia_c = ImpactType(code='C', name='Confidentiality',
                        metrics={
                            xit_xcia_c_n.code: xit_xcia_c_n,
                            xit_xcia_c_l.code: xit_xcia_c_l,
                            xit_xcia_c_h.code: xit_xcia_c_h
                        })

xit_xcia_i_n = Metric(code='N', index=1, name='None')
xit_xcia_i_l = Metric(code='L', index=2, name='Low')
xit_xcia_i_h = Metric(code='H', index=3, name='High')
xit_xcia_i = ImpactType(code='I', name='Integrity',
                        metrics={
                            xit_xcia_i_n.code: xit_xcia_i_n,
                            xit_xcia_i_l.code: xit_xcia_i_l,
                            xit_xcia_i_h.code: xit_xcia_i_h
                        })

xit_xcia_a_n = Metric(code='N', index=1, name='None')
xit_xcia_a_l = Metric(code='L', index=2, name='Low')
xit_xcia_a_h = Metric(code='H', index=3, name='High')
xit_xcia_a = ImpactType(code='A', name='Availability ',
                        metrics={
                            xit_xcia_a_n.code: xit_xcia_a_n,
                            xit_xcia_a_l.code: xit_xcia_a_l,
                            xit_xcia_a_h.code: xit_xcia_a_h
                        })

xit_xcia = ImpactType(code='XCIA', name='Original CIA',
                      description='Original CVSS v3.1 CIA (Confidentiality, Integrity, Availability) Impact',
                      metrics={
                          xit_xcia_c.code: xit_xcia_c,
                          xit_xcia_i.code: xit_xcia_i,
                          xit_xcia_a.code: xit_xcia_a
                      })

# Patient Safety (XPS)

xit_xps_n = Metric(code='N', index=1, name='Negligible')
xit_xps_l = Metric(code='L', index=2, name='Limited')
xit_xps_md = Metric(code='MD', index=3, name='Moderate')
xit_xps_mj = Metric(code='MJ', index=4, name='Major')
xit_xps_c = Metric(code='C', index=5, name='Critical')
xit_xps = ImpactType(code='XPS', name='Patient Safety',
                     description='Harm caused to the patient',
                     metrics={
                         xit_xps_n.code: xit_xps_n,
                         xit_xps_l.code: xit_xps_l,
                         xit_xps_md.code: xit_xps_md,
                         xit_xps_mj.code: xit_xps_mj,
                         xit_xps_c.code: xit_xps_c
                     })

# Sensitive Data Exposure (XSD)

xit_xsd_n = Metric(code='N', index=1, name='None')  # FIXME: Change ML INDEX order  to: SL, PL, SG, PG
xit_xsd_sl = Metric(code='SL', index=2, name='Secondary Less')  # 'Secondary Personal Identifiers, Less than 10,000'
xit_xsd_pl = Metric(code='PL', index=3, name='Primary Less')  # 'Primary Personal Identifiers, Less than 10,000'
xit_xsd_sg = Metric(code='SG', index=4,
                    name='Secondary Greater')  # 'Secondary Personal Identifiers, Greater than 10,000'
xit_xsd_pg = Metric(code='PG', index=5, name='Primary Greater')  # 'Primary Personal Identifiers, Greater than 10,000'
xit_xsd = ImpactType(code='XSD', name='Sensetive Data Exposure',
                     description='Amount of Personal (PII/PHI) records exposed',
                     metrics={
                         xit_xsd_n.code: xit_xsd_n,
                         xit_xsd_sl.code: xit_xsd_sl,
                         xit_xsd_pl.code: xit_xsd_pl,
                         xit_xsd_sg.code: xit_xsd_sg,
                         xit_xsd_pg.code: xit_xsd_pg
                     })


# Hospital Breach (XHB)

xit_xhb_n = Metric(code='N', index=1, name='None')
xit_xhb_da = Metric(code='DA', index=2, name='Device Availability')
xit_xhb_na = Metric(code='NA', index=3, name='Network Access')
xit_xhb_ui = Metric(code='UI', index=4, name='User Impersonation')
xit_xhb = ImpactType(code='XHB', name='Hospital Breach',
                     description='Potential for successful hospital attack based of MDM product compromise',
                     metrics={
                         xit_xhb_n.code: xit_xhb_n,
                         xit_xhb_da.code: xit_xhb_da,
                         xit_xhb_na.code: xit_xhb_na,
                         xit_xhb_ui.code: xit_xhb_ui
                     })

impact_types = ImpactTypes(code='XIT', name='Impact Types',
                           description='The direct consequence of a successful exploit, and represent '
                                       'the consequence of the thing that suffers the impact, '
                                       'which we refer to formally as the impacted component',
                           metrics={
                               xit_xcia.code: xit_xcia,
                               xit_xps.code: xit_xps,
                               xit_xsd.code: xit_xsd,
                               xit_xhb.code: xit_xhb
                           })

metric_group_base = MetricGroup(code='BASE', name='Base Metric Group',
                                description='The Base metric group represents the intrinsic characteristics of '
                                            'a vulnerability that are constant over time and across user environments. '
                                            'It is composed of two sets of metrics: the Exploitability metrics and '
                                            'the Impact metrics.',
                                metrics={
                                    metric_group_exp.code: metric_group_exp,
                                    impact_types.code: impact_types,

                                })

metric_codes = MetricCode(
    EXP=metric_group_exp.code,
    XIT=impact_types.code,
    XCIA=xit_xcia.code,
    XPS=xit_xps.code,
    XSD=xit_xsd.code,
    XHB=xit_xhb.code)
