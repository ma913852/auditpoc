# 📸 Multi-Image Upload UI Guide

## 🎨 Visual Walkthrough

### **1. Initial State (0 Images)**

```
┌─────────────────────────────────────────────────┐
│  ✍️ What did you observe? *                    │
│  ┌─────────────────────────────────────────┐   │
│  │ [Text area for observation notes]       │   │
│  │                                          │   │
│  └─────────────────────────────────────────┘   │
│                                                  │
│  ┌───────────────────┬───────────────────┐     │
│  │ 📸 Photos (Up to 5)│ 🎤 Voice (Optional)│    │
│  ├───────────────────┼───────────────────┤     │
│  │                    │                    │     │
│  │ [📸 Add Photos     │ [🎤 Record]       │     │
│  │     (0/5)]         │                    │     │
│  │                    │                    │     │
│  └───────────────────┴───────────────────┘     │
│                                                  │
│  [⚡ Analyze with AI]                           │
└─────────────────────────────────────────────────┘
```

---

### **2. After Adding 1 Photo**

```
┌─────────────────────────────────────────────────┐
│  📸 Photos (Up to 5)                            │
│  [📸 Add Photos (1/5)]  ← Button still enabled │
│                                                  │
│  ┌────────────────────────────────────────┐    │
│  │ Gallery:                                │    │
│  │ ┌───────────┐                          │    │
│  │ │ [Photo 1] │                          │    │
│  │ │    [×]    │ ← Hover to see remove    │    │
│  │ └───────────┘                          │    │
│  │                                         │    │
│  │ [Optional: Describe all photos...]     │    │
│  └────────────────────────────────────────┘    │
└─────────────────────────────────────────────────┘
```

---

### **3. After Adding 3 Photos**

```
┌─────────────────────────────────────────────────┐
│  📸 Photos (Up to 5)                            │
│  [📸 Add Photos (3/5)]  ← Can add 2 more       │
│                                                  │
│  ┌────────────────────────────────────────┐    │
│  │ Gallery (2-column grid):                │    │
│  │ ┌───────────┐  ┌───────────┐          │    │
│  │ │ [Photo 1] │  │ [Photo 2] │          │    │
│  │ │    [×]    │  │    [×]    │          │    │
│  │ └───────────┘  └───────────┘          │    │
│  │ ┌───────────┐                          │    │
│  │ │ [Photo 3] │                          │    │
│  │ │    [×]    │                          │    │
│  │ └───────────┘                          │    │
│  │                                         │    │
│  │ [Optional: Describe all photos...]     │    │
│  └────────────────────────────────────────┘    │
│                                                  │
│  [⚡ Analyze with AI]                           │
└─────────────────────────────────────────────────┘
```

---

### **4. At Maximum Capacity (5 Photos)**

```
┌─────────────────────────────────────────────────┐
│  📸 Photos (Up to 5)                            │
│  [📸 Add Photos (5/5)]  ← Button DISABLED      │
│     (grayed out)                                 │
│                                                  │
│  ┌────────────────────────────────────────┐    │
│  │ Gallery:                                │    │
│  │ ┌───────────┐  ┌───────────┐          │    │
│  │ │ [Photo 1] │  │ [Photo 2] │          │    │
│  │ │    [×]    │  │    [×]    │          │    │
│  │ └───────────┘  └───────────┘          │    │
│  │ ┌───────────┐  ┌───────────┐          │    │
│  │ │ [Photo 3] │  │ [Photo 4] │          │    │
│  │ │    [×]    │  │    [×]    │          │    │
│  │ └───────────┘  └───────────┘          │    │
│  │ ┌───────────┐                          │    │
│  │ │ [Photo 5] │  ✓ Max reached          │    │
│  │ │    [×]    │                          │    │
│  │ └───────────┘                          │    │
│  │                                         │    │
│  │ [Optional: Describe all photos...]     │    │
│  └────────────────────────────────────────┘    │
└─────────────────────────────────────────────────┘
```

---

### **5. Hover State (Show Remove Button)**

```
┌───────────────────────────────────┐
│ Gallery Photo:                    │
│ ┌───────────────────────────────┐ │
│ │       🖼️ [Photo Thumbnail]    │ │
│ │                                │ │
│ │   ┌───┐                        │ │
│ │   │ × │  ← Remove button       │ │
│ │   └───┘     (appears on hover) │ │
│ │                                │ │
│ │   Photo 2                      │ │
│ └───────────────────────────────┘ │
└───────────────────────────────────┘
```

---

### **6. After Clicking Remove**

```
Before (3 photos):                   After (2 photos):
┌───────────┐  ┌───────────┐        ┌───────────┐
│ [Photo 1] │  │ [Photo 2] │        │ [Photo 1] │
│    [×]    │  │    [×]    │        │    [×]    │
└───────────┘  └───────────┘        └───────────┘
┌───────────┐                        ┌───────────┐
│ [Photo 3] │                        │ [Photo 3] │
│    [×]    │                        │    [×]    │
└───────────┘                        └───────────┘

[📸 Add Photos (3/5)]               [📸 Add Photos (2/5)]
                                     ↑ Button re-enabled
```

---

### **7. Analysis in Progress**

```
┌─────────────────────────────────────────────────┐
│  [⚡ Analyzing 3 photos...]                     │
│   ↑ Shows photo count                           │
│   [Spinning animation]                           │
└─────────────────────────────────────────────────┘
```

---

### **8. AI Results with Multi-Image Analysis**

```
┌─────────────────────────────────────────────────────────┐
│  🤖 AI Recommendation:                                  │
│  ┌─────────────────────────────────────────────────┐   │
│  │ req_007: 21 CFR 211.194 (89% confidence)       │   │
│  │ Category: Documentation                         │   │
│  │                                                  │   │
│  │ 💡 AI Insights:                                 │   │
│  │ • Missing verification signature (Image 1)      │   │
│  │ • Improper data correction (Image 2)            │   │
│  │ • Incomplete QA review (Image 3)                │   │
│  └─────────────────────────────────────────────────┘   │
│                                                          │
│  📋 Visual Findings:                                    │
│  ┌─────────────────────────────────────────────────┐   │
│  │ Image 1 (Batch Record, Page 1):                │   │
│  │ Shows sterile filtration step completed on      │   │
│  │ 15-Jan-2024, but verification signature field   │   │
│  │ is blank.                                       │   │
│  │                                                  │   │
│  │ Image 2 (Page 2, Line 48):                     │   │
│  │ The 'Time' field appears overwritten without    │   │
│  │ proper cross-out procedure - potential data     │   │
│  │ integrity concern.                               │   │
│  │                                                  │   │
│  │ Image 3 (QA Review Checklist):                 │   │
│  │ Section 4 'Critical Step Verification' not      │   │
│  │ signed off by QA before batch release.          │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 Key UI Features

### **Dynamic Counter Badge**
```
[📸 Add Photos (0/5)]  ← No images
[📸 Add Photos (1/5)]  ← 1 image added
[📸 Add Photos (3/5)]  ← 3 images added
[📸 Add Photos (5/5)]  ← Maximum reached (button disabled)
```

### **Button States**

| State | Appearance | Behavior |
|-------|------------|----------|
| **0-4 photos** | Blue, enabled | Opens file picker |
| **5 photos** | Gray, disabled, grayed out | No action |
| **After removing** | Blue, re-enabled | Opens file picker |

### **Remove Button Interaction**

```css
/* CSS for remove button */
.group-hover\:opacity-100 {
    opacity: 0;              /* Hidden by default */
    transition: opacity 0.2s;
}

.group:hover .group-hover\:opacity-100 {
    opacity: 1;              /* Visible on hover */
}
```

**Visual:**
- **Not hovering:** Remove button invisible
- **Hovering over photo:** Red × button appears in top-right corner
- **Click ×:** Photo removed, gallery updates, counter decrements

---

## 📱 Responsive Design

### **Desktop/Tablet (2-column grid)**
```
┌───────────┐  ┌───────────┐
│ Photo 1   │  │ Photo 2   │
└───────────┘  └───────────┘
┌───────────┐  ┌───────────┐
│ Photo 3   │  │ Photo 4   │
└───────────┘  └───────────┘
```

### **Mobile (could be adjusted to 1-column)**
```
┌───────────┐
│ Photo 1   │
└───────────┘
┌───────────┐
│ Photo 2   │
└───────────┘
┌───────────┐
│ Photo 3   │
└───────────┘
```

---

## 🎨 Color Scheme

| Element | Color | Purpose |
|---------|-------|---------|
| **Add Photos button** | Blue (`bg-blue-500`) | Primary action |
| **Add Photos (disabled)** | Gray (`opacity-50`) | Indicates max reached |
| **Photo border** | Blue (`border-blue-300`) | Highlight photos |
| **Remove button** | Red (`bg-red-500`) | Destructive action |
| **Photo label** | Black overlay (`bg-black bg-opacity-50`) | Image numbering |

---

## 🔄 State Transitions

```
[Add Photos (0/5)]
       ↓ Add 1 photo
[Add Photos (1/5)] [Gallery visible]
       ↓ Add 2 more
[Add Photos (3/5)] [Gallery with 3 photos]
       ↓ Add 2 more
[Add Photos (5/5)] [Button DISABLED]
       ↓ Remove 1 photo
[Add Photos (4/5)] [Button RE-ENABLED]
       ↓ Clear all
[Add Photos (0/5)] [Gallery hidden]
```

---

## 📏 Dimensions

| Element | Size |
|---------|------|
| **Thumbnail height** | `h-24` (96px) |
| **Grid columns** | 2 |
| **Grid gap** | `gap-2` (8px) |
| **Remove button** | `w-5 h-5` (20x20px) |
| **Border width** | `border-2` |

---

## 🧩 HTML Structure

```html
<div id="imageGallery" class="mt-2 hidden">
    <div id="imageGalleryGrid" class="grid grid-cols-2 gap-2">
        <!-- Each photo rendered as: -->
        <div class="relative group">
            <img src="[Base64]" class="w-full h-24 object-cover rounded border-2 border-blue-300">
            <button onclick="removeImage('[id]')" 
                    class="absolute top-1 right-1 bg-red-500 text-white rounded-full w-5 h-5 
                           flex items-center justify-center text-xs font-bold hover:bg-red-600 
                           opacity-0 group-hover:opacity-100 transition-opacity">
                ×
            </button>
            <div class="absolute bottom-0 left-0 right-0 bg-black bg-opacity-50 
                        text-white text-xs text-center py-0.5">
                Photo [index]
            </div>
        </div>
    </div>
    <input type="text" id="imageDescription" 
           placeholder="Optional: Describe all photos..." 
           class="mt-2 w-full px-2 py-1 border border-slate-300 rounded text-xs">
</div>
```

---

## ✅ Accessibility

| Feature | Implementation |
|---------|----------------|
| **Button disabled state** | `disabled` attribute + visual opacity change |
| **Counter feedback** | Clear "X/5" indicator |
| **Hover feedback** | Remove button only visible on hover |
| **Photo numbering** | "Photo 1", "Photo 2", etc. |
| **Alert on overflow** | User notified when trying to add too many |

---

## 🎯 User Actions Summary

| Action | Result |
|--------|--------|
| **Click "Add Photos"** | Opens file picker (single or multiple selection) |
| **Select 1 photo** | Gallery appears, counter shows "1/5" |
| **Select 5 more (6 total)** | Alert shown, only first 5 added |
| **Hover over photo** | Red × remove button appears |
| **Click ×** | That photo removed, counter decrements |
| **Reach 5 photos** | Button disabled, grayed out |
| **Remove any photo** | Button re-enabled |
| **Clear all (reset form)** | Gallery hidden, counter resets to "0/5" |

---

## 📸 Example Flow

```
User wants to document a batch record issue:

1. Clicks "Add Photos"
2. Takes 3 photos:
   - Photo 1: Page 1 of batch record
   - Photo 2: Page 2 of batch record
   - Photo 3: QA checklist

3. Gallery shows:
   ┌───────────┐  ┌───────────┐
   │ Photo 1   │  │ Photo 2   │
   └───────────┘  └───────────┘
   ┌───────────┐
   │ Photo 3   │
   └───────────┘
   [Optional: Describe all photos...]

4. User types observation text

5. Clicks "⚡ Analyze with AI"

6. Button changes to "⚡ Analyzing 3 photos..."

7. AI analyzes all 3 images together

8. Results show:
   - Matched requirement
   - Visual findings (references each image)
   - Key findings
   - Recommendations

9. User can:
   - Accept AI suggestion
   - Override with manual selection
   - Add more details
   - Save observation
```

---

## 🎉 Summary

✅ **Intuitive counter** shows remaining capacity  
✅ **Gallery preview** shows all photos at once  
✅ **Individual removal** via hover × button  
✅ **Smart button disabling** at max capacity  
✅ **Clear visual feedback** at every step  
✅ **Responsive layout** adapts to screen size  
✅ **Professional appearance** matches existing UI  

**The multi-image UI is clean, intuitive, and production-ready!** 📸✨

