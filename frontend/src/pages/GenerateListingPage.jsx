import { useMemo, useState } from 'react'

import InputField from '../components/InputField'
import { generateListing } from '../lib/api'

const initialForm = {
  product_name: '',
  brand_name: '',
  category: '',
  material: '',
  color: '',
  dimensions: '',
  weight: '',
  key_features: '',
  target_customer: '',
  use_case: '',
  primary_keywords: '',
  secondary_keywords: '',
}

export default function GenerateListingPage() {
  const [form, setForm] = useState(initialForm)
  const [files, setFiles] = useState([])
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)

  const parsedPayload = useMemo(() => ({
    ...form,
    key_features: form.key_features ? form.key_features.split(',').map((v) => v.trim()) : [],
    primary_keywords: form.primary_keywords ? form.primary_keywords.split(',').map((v) => v.trim()) : [],
    secondary_keywords: form.secondary_keywords ? form.secondary_keywords.split(',').map((v) => v.trim()) : [],
  }), [form])

  const handleChange = (e) => setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }))

  const handleGenerate = async () => {
    setLoading(true)
    try {
      const data = await generateListing(parsedPayload, files)
      setResult(data)
    } finally {
      setLoading(false)
    }
  }

  const copySection = async (text) => navigator.clipboard.writeText(text)

  const downloadPdf = () => {
    if (!result) return
    const content = [
      `Title: ${result.listing.title}`,
      `Bullets:\n${result.listing.bullet_points.map((b) => `- ${b}`).join('\n')}`,
      `Description:\n${result.listing.description}`,
      `Backend Terms: ${result.listing.backend_search_terms}`,
      `Image Captions:\n${result.listing.image_captions.map((c) => `- ${c}`).join('\n')}`,
    ].join('\n\n')
    const blob = new Blob([content], { type: 'application/pdf' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'amazon-listing.pdf'
    a.click()
    URL.revokeObjectURL(url)
  }

  const sections = result
    ? [
        { title: 'Title', content: result.listing.title },
        { title: 'Bullet Points', content: result.listing.bullet_points.join('\n') },
        { title: 'Description', content: result.listing.description },
        { title: 'Backend Keywords', content: result.listing.backend_search_terms },
        { title: 'Image Captions', content: result.listing.image_captions.join('\n') },
      ]
    : []

  return (
    <div className="p-6 md:p-8 text-white space-y-6 overflow-auto h-screen">
      <h2 className="text-2xl font-semibold">Generate Amazon India Listing</h2>

      <div className="grid lg:grid-cols-2 gap-6">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
          <h3 className="font-medium">Optional Product Details</h3>
          <div className="grid sm:grid-cols-2 gap-3">
            {Object.keys(initialForm).map((key) => (
              <InputField
                key={key}
                label={key.replaceAll('_', ' ')}
                name={key}
                value={form[key]}
                onChange={handleChange}
                placeholder={`Enter ${key.replaceAll('_', ' ')}`}
              />
            ))}
          </div>
          <div>
            <p className="text-sm text-slate-300 mb-1">Product Images (JPG/PNG/WEBP)</p>
            <input
              type="file"
              multiple
              accept="image/jpeg,image/png,image/webp"
              onChange={(e) => setFiles(Array.from(e.target.files || []))}
              className="text-sm"
            />
          </div>
          <button
            onClick={handleGenerate}
            disabled={loading}
            className="w-full bg-indigo-600 hover:bg-indigo-500 py-2 rounded-lg font-medium"
          >
            {loading ? 'Generating...' : 'Generate Listing'}
          </button>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
          <h3 className="font-medium">Generated Output</h3>
          {!result && <p className="text-slate-400 text-sm">Results appear here after generation.</p>}

          {sections.map((section) => (
            <div key={section.title} className="border border-slate-800 rounded-lg p-3">
              <div className="flex items-center justify-between mb-2">
                <h4 className="font-medium text-indigo-300">{section.title}</h4>
                <div className="space-x-2">
                  <button
                    onClick={() => copySection(section.content)}
                    className="text-xs px-2 py-1 bg-slate-800 rounded"
                  >
                    Copy text
                  </button>
                  <button className="text-xs px-2 py-1 bg-slate-800 rounded">Edit content</button>
                </div>
              </div>
              <pre className="whitespace-pre-wrap text-sm text-slate-200">{section.content}</pre>
            </div>
          ))}

          {result && (
            <button onClick={downloadPdf} className="w-full bg-emerald-600 hover:bg-emerald-500 py-2 rounded-lg">
              Download PDF
            </button>
          )}
        </div>
      </div>
    </div>
  )
}
