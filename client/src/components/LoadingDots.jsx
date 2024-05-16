import styles from './loading-dots.module.css';

const LoadingDots = ({ message = null, color = '#000' }) => {
    return (
        <div>
            <span>{message}</span>
            <span className={styles.loading}>
                <span style={{ backgroundColor: color }} />
                <span style={{ backgroundColor: color }} />
                <span style={{ backgroundColor: color }} />
            </span>
        </div>
    );
};

export default LoadingDots;