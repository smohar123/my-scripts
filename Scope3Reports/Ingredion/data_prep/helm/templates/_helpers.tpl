{{/* podSpecPatch for setting ephemeral storage for non-container workflow components */}}
{{- define "carver.ephemeralStorage" }}
podSpecPatch: |
  containers:
    - name: main
      resources:
        limits:
          ephemeral-storage: "{{ .Values.defaultEphemeralStorageSize }}"
{{- end }}}

{{/* Standard argument parameters for carver scala image */}}
{{- define "carver.image" }}{{ .Values.global.awsAccountId }}.dkr.ecr.{{ .Values.awsRegion }}.amazonaws.com/{{ .Values.image.repoName }}:{{ .Values.image.tag }}{{- end }}

{{/* Standard argument parameters for carver python qa image */}}
{{- define "carver.qaImage" }}{{ .Values.global.awsAccountId }}.dkr.ecr.{{ .Values.awsRegion }}.amazonaws.com/{{ .Values.qaImage.repoName }}:{{ .Values.qaImage.tag }}{{- end }}


{{/* Standard argument parameters for geomancer, sylvester and cropnosis */}}
{{- define "carver.serviceDependencyParams" }}
- name: geomancerHost
  value: "geomancer.geomancer-{{ .Values.ciboEnvironment }}.svc.cluster.local"
- name: geomancerPort
  value: {{ .Values.geomancer.port }}
- name: sylvesterUri
  value: "http://sylvester-{{ .Values.ciboEnvironment }}.sylvester-{{ .Values.ciboEnvironment }}.svc.cluster.local"
- name: cropnosisUri
  value: "http://cropnosis-{{ .Values.ciboEnvironment }}.cropnosis-{{ .Values.ciboEnvironment }}.svc.cluster.local"
{{- end }}

{{/* Encapsulate bucket suffic logic */}}
{{- define "carver.s3Bucket" }}{{ .Values.s3Bucket }}{{- if .Values.awsBucketSuffix }}{{ .Values.awsBucketSuffix }}{{- end }}{{- end }}