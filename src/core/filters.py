import cv2

def none_filter(img, intensity):
    return cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)

def limiar_filter(img, intensity):
    gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
    _, thresh = cv2.threshold(gray, intensity, 255, cv2.THRESH_BINARY)
    return thresh

def canny_filter(img, intensity):
    gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
    edges = cv2.Canny(gray, intensity, intensity + 100)
    return edges

AVAILABLE_FILTERS = {
    "None": none_filter,
    "Limiar": limiar_filter
    #"Edge (Canny)": canny_filter
}