# test typechat in python
out:
```
{
  "title": "表格",
  "gridPos": {
    "x": 0,
    "y": 0,
    "h": 1,
    "w": 1,
    "i": "init"
  },
  "dependParams": [],
  "style": null,
  "outputs": [],
  "refreshInterval": null,
  "visibleExp": null,
  "uniqueKey": "a4b7a54d-02b4-415e-8913-08b677ac59ec",
  "api": {
    "url": "http://baidu.com",
    "paging": false
  },
  "columns": [
    {
      "dataIndex": "label",
      "label": "标签"
    },
    {
      "dataIndex": "value",
      "label": "值",
      "render": "<a href='$(row.label)'>$(row.value)</a>"
    },
    {
      "dataIndex": "number",
      "label": "数字"
    }
  ],
  "size": "small"
}

```