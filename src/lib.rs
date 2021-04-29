use askalono::{Store, TextData};
use pyo3::prelude::*;
use pyo3::wrap_pyfunction;

static CACHE_DATA: &[u8] = include_bytes!("../embedded-cache.bin.zstd");

fn load_store() -> Store {
    Store::from_cache(CACHE_DATA).expect("Cannot load built-in store")
}

#[pyclass]
struct License {
    #[pyo3(get)]
    score: f32,
    #[pyo3(get)]
    name: String,
}

#[pyfunction]
fn identify(license_text: &str) -> PyResult<License> {
    let store = load_store();
    let m = store.analyze(&TextData::from(license_text));
    let license: License = License {
        score: m.score,
        name: m.name.to_string(),
    };
    Ok(license)
}

#[pymodule]
fn askalono(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<License>()?;
    m.add_function(wrap_pyfunction!(identify, m)?)?;

    Ok(())
}
