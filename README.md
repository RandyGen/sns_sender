# massage sender to some SNSs
I created app to send same message to "TypeTalk" and "Slack" for Python.

I'll update other SNSs (ex Twitter...).

## Options
<dl>
  <dt>--massage</dt>
  <dd>message which you'd like to send</dd>
  <dt>--sns_type</dt>
  <dd>
  SNS which you'd like to use

  you can choose one in "slack", "typetalk", "all(all SNSs)"
  </dd>
</dl>

## Execution App
```python
python sender.py --message hello --sns_type all
```

```sh
sh sender.sh 
```

## Reference
- [typetalk api](https://qiita.com/shio_sa1t/items/e61fa584c0c76b6782d1)
- [slack api](https://developers.wonderpla.net/entry/2020/06/18/110005)