{{- define "sciforge.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "sciforge.fullname" -}}
{{- printf "%s-%s" .Release.Name (include "sciforge.name" .) | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "sciforge.labels" -}}
app.kubernetes.io/name: {{ include "sciforge.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
