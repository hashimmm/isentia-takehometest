import sqlalchemy as sa


engine = sa.create_engine("postgresql://isentia:isentia@postgres/isentia", echo=False, future=True)
m = sa.MetaData()
news_tbl = sa.Table('news', m,
    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('org', sa.Text, nullable=False),
    sa.Column('dt_fetched', sa.DateTime(timezone=True)),
    sa.Column('url', sa.Text, nullable=False),
    sa.Column('content', sa.JSON, nullable=False)
)
sa.Index('idx_org_dt', news_tbl.c.org, sa.desc(news_tbl.c.dt_fetched))

def ensure_table(engine):
    m.create_all(engine, checkfirst=True)

def clear_table(engine):
    with engine.connect() as conn:
        conn.execute(news_tbl.delete().where(True))
        conn.commit()
