SELECT * FROM crolections.izbori2015 where izbori2015_source=1;

#broj tvitova po korisniku
select izbori2015_user, count(*) from izbori2015 group by izbori2015_user;

#odgovori korisniku, malo podataka
select izbori2015_user_id, count(*) from izbori2015 where izbori2015_in_reply_to_user_id != 0 group by izbori2015_user_id;

#odgovori na tvit status
select izbori2015_user_id, count(*) from izbori2015 where izbori2015_in_reply_to_user_id != 0 group by izbori2015_user_id;

#tvitovi sa linkovima
select count(*) from izbori2015 where izbori2015_URLs != '';

#tvitovi po danu
SELECT  DATE(izbori2015_created_at) datum, COUNT(DISTINCT izbori2015_tweet_id) totalCOunt
FROM    izbori2015
GROUP   BY  datum;

#ritvitani tvitovi
select * from izbori2015 where izbori2015_retweet_count != 0;

#ne pocinju sa RT -> nisu retvits (dakle, nema ponavljanja sadrzaja)
select * from izbori2015 where izbori2015_text not like 'RT%';

#distinct users
select count(distinct(izbori2015_user)) from izbori2015;

#
select count(*) from izbori2015 where DATE(izbori2015_created_at)=DATE(2015-01-10);

select date(izbori2015_created_at), count(*) from izbori2015 group by date(izbori2015_created_at);

select izbori2015_user, count(*) from izbori2015 WHERE DATE(izbori2015_created_at) > DATE(2015-08-08) group by izbori2015_user;

#RANGE
select count(*) from (
	select izbori2015_user, count(*) as cstar  from izbori2015 group by izbori2015_user
) as t where t.cstar <= 20;

#LDA GROUPS
SELECT lda, count(*) as nrDocuments FROM crolections.rezultati group by lda ORDER BY nrDocuments desc;