"""
data/spec_documents.py — synthetic spec corpus for the Q&A engine.

7 documents map 1:1 to the 7 requirement types in spec_registry.py, written
as real spec-clause-style prose (the kind of paragraph you'd actually find in
a data-centre EPC specification section). 3 additional documents cover
adjacent-but-different topics -- these exist specifically to test that the
engine doesn't false-match a plausible-sounding but wrong clause, and that
genuinely out-of-corpus questions get silence rather than a stretched match.
"""

from qa_engine import Document

SPEC_DOCUMENTS = [
    Document(
        doc_id="ups_runtime",
        title="Section 26 33 53 - UPS Battery Autonomy",
        text=(
            "The uninterruptible power supply system shall provide a minimum "
            "battery runtime of 15 minutes at full rated load before transfer "
            "to standby generation is required. Runtime shall be verified by "
            "load-bank test and documented in the commissioning report."
        ),
    ),
    Document(
        doc_id="ups_efficiency",
        title="Section 26 33 53 - UPS Electrical Efficiency",
        text=(
            "UPS modules shall achieve a minimum electrical conversion "
            "efficiency of 96 percent when operating at rated load, measured "
            "in double-conversion online mode per manufacturer test data "
            "submitted with the equipment submittal."
        ),
    ),
    Document(
        doc_id="wue",
        title="Section 23 00 00 - Water Usage Effectiveness (WUE) Target",
        text=(
            "The mechanical cooling system design shall achieve an annualized "
            "Water Usage Effectiveness of 0.20 liters per kilowatt-hour or "
            "better, calculated per The Green Grid WUE methodology, favoring "
            "air-side or water-side economization over cooling-tower makeup "
            "water consumption."
        ),
    ),
    Document(
        doc_id="cooling_cycles",
        title="Section 23 25 00 - Condenser Water Cycles of Concentration",
        text=(
            "Condenser water chemistry shall be maintained between 3 and 6 "
            "cycles of concentration. Operation below 3 cycles indicates "
            "excessive blowdown and water waste; operation above 6 cycles "
            "risks scale formation and corrosion on heat-exchange surfaces."
        ),
    ),
    Document(
        doc_id="waste_heat_recovery",
        title="Section 23 52 00 - Waste-Heat Recovery System",
        text=(
            "A minimum of 10 percent of total rejected heat from the "
            "mechanical plant shall be captured and reused, whether for "
            "adjacent building heating, domestic hot water preheat, or an "
            "equivalent beneficial-use application documented in the design "
            "narrative."
        ),
    ),
    Document(
        doc_id="generator_load",
        title="Section 26 32 13 - Standby Generator Load-Bank Testing",
        text=(
            "Standby generators shall be load-bank tested between 30 percent "
            "and 80 percent of rated nameplate capacity. Sustained operation "
            "below 30 percent risks wet-stacking from incomplete combustion; "
            "operation above 80 percent leaves insufficient headroom for "
            "step loads during an N+1 failover event."
        ),
    ),
    Document(
        doc_id="ggbs",
        title="Section 03 30 00 - GGBS Cement Replacement in Structural Concrete",
        text=(
            "Structural concrete mix designs shall incorporate Ground "
            "Granulated Blast-furnace Slag (GGBS) as cement replacement at a "
            "rate of 30 to 50 percent by mass, balancing embodied-carbon "
            "reduction against early-strength development needed to hold the "
            "construction schedule."
        ),
    ),
    # -- adjacent-but-different topics, to test discrimination and silence --
    Document(
        doc_id="site_security_fencing",
        title="Section 32 31 00 - Perimeter Security Fencing",
        text=(
            "Perimeter fencing shall be a minimum of 2.4 meters in height "
            "with anti-climb mesh and shall be inspected quarterly for "
            "integrity as part of the physical security program."
        ),
    ),
    Document(
        doc_id="employee_parking",
        title="Section 01 50 00 - Temporary Construction Parking",
        text=(
            "Contractor personnel parking during the construction period "
            "shall be designated in the lay-down area shown on drawing "
            "C-102 and shall not obstruct the fire lane at any time."
        ),
    ),
    Document(
        doc_id="fire_suppression",
        title="Section 21 20 00 - Clean Agent Fire Suppression",
        text=(
            "The white space shall be protected by a clean-agent fire "
            "suppression system sized for the room volume, with a minimum "
            "hold time of 10 minutes and cross-zone smoke detection required "
            "for pre-action discharge."
        ),
    ),
]

assert len(SPEC_DOCUMENTS) == 10
assert len({d.doc_id for d in SPEC_DOCUMENTS}) == 10, "duplicate doc_id in corpus"
