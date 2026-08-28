{{- $docs := where .Site.RegularPages "Type" "docs" -}}
{{- $docs = where $docs ".Params.toc_hide" "!=" true -}}
{{- $docs = where $docs ".Params.sidebar_divider" "!=" true -}}
{{- $docs = where $docs ".Params.manuallink" "==" nil -}}
{{- $zh := eq .Site.Language.Lang "zh" -}}
{{- $llmsURL := "llms.txt" | relURL -}}
{{- with .OutputFormats.Get "LLMS" }}{{ $llmsURL = .RelPermalink }}{{ end -}}
# {{ .Title | strings.TrimSpace }}

{{ with .Description | strings.TrimSpace -}}
> {{ replace . "\n" "\n> " }}
{{ end }}

{{ cond $zh "LLMS 索引：" "LLMS index: " }}[llms.txt]({{ $llmsURL }})

{{ with .RenderShortcodes | strings.TrimSpace -}}
{{ . }}
{{ end }}

## {{ cond $zh "文档索引" "Documentation index" }}

{{ range $docs.ByWeight -}}
{{- $url := .Permalink -}}
{{- with .OutputFormats.Get "markdown" }}{{ $url = .Permalink }}{{ end -}}
- [{{ .Title }}]({{ $url }}){{ with .Description }}: {{ . | strings.TrimSpace | replaceRE `\s+` " " }}{{ end }}
{{ end }}
{{ range slice "blog/design" "blog/release" -}}
{{- with $.Site.GetPage . -}}
{{- $url := .Permalink -}}
{{- with .OutputFormats.Get "markdown" }}{{ $url = .Permalink }}{{ end }}
- [{{ .Title }}]({{ $url }}): {{ .Description }}
{{- end }}
{{ end -}}
