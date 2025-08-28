"""
`Record` represents a Program's health and financials in a monthly snapshot, captured
through the `Program Performance Review (PPR)` Tool. These snapshots encompass both the subjective
analysis provided by a `Program Manager` or `Program Financial Analyst` and numerous metrics that 
detail the health of the `Program`. Each `Record` includes a variety of attributes, such as 
financial performance, technical assessment, risk assessment, and other key indicators of program 
health. The PPR Tool leverages `Record` data to generate comprehensive reports, primarily in the 
form of PowerBI Dashboards, that summarize the state and progress of a `Program` over time. These 
reports provide valuable insights for stakeholders, enabling them to track the evolution of a 
`Program` and make informed decisions based on historical performance and trends.
By maintaining a detailed log of records, users can gain a holistic view of a 
`Program`'s health and effectively manage its progress. 
"""

from program_review_tool.models.Record.Record import Record
